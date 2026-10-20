"""Bağlantılar ekranının denetleyicisi (ADR-0014): kart eylemleri, yoklamalar, anahtarlar.

Ana pencereyle (`App`) yalnızca küçük bir arayüzle konuşur: tercihleri kaydetme, ayarları
yeniden uygulama, arka plan görevi başlatma ve bildirim gösterme.
"""

from __future__ import annotations

import asyncio
import os
from typing import TYPE_CHECKING, Any, cast

from codementor.desktop.bridge import Cancellation, Emit, Message
from codementor.desktop.connections import (
    INFO,
    PROVIDERS,
    TOOL_AGENTS,
    KeyStore,
    KeyStoreError,
    Probe,
    apply_key,
    key_env,
    key_source,
    load_vault_keys,
    model_suggestions,
    probe,
    try_connection,
)
from codementor.desktop.login import LoginUnavailableError, open_login_console
from codementor.desktop.services import (
    OllamaPullError,
    PullOutcome,
    compiler_statuses,
    compiler_update_available,
    describe_progress,
    offer_compiler_download,
    ollama_pull_argv,
    run_ollama_pull,
)
from codementor.desktop.widgets.provider_card import CardActions
from codementor.models.api import CompilerStatus
from codementor.models.desktop import ProviderOverride
from codementor.models.provider import ProviderStatus
from codementor.models.validation import DownloadProgress
from codementor.providers.base import ProviderError
from codementor.validation.toolchain import clear_toolchain_cache
from codementor.validation.toolchain_install import InstallCancelledError, install_zig

if TYPE_CHECKING:
    from codementor.desktop.app import App
    from codementor.desktop.views.connections_view import ConnectionsView


class ConnectionsController:
    def __init__(self, app: App, store: KeyStore) -> None:
        self.app = app
        self.store = store
        self.suggestions = model_suggestions()
        self.discovered: dict[str, list[str]] = {}
        self.probes: dict[str, Probe] = {}
        self.vaulted = load_vault_keys(app.settings.providers, store)
        self.view: ConnectionsView | None = None
        self.download_cancellation: Cancellation | None = None
        self._pull_cancellations: dict[str, Cancellation] = {}

    def actions(self) -> CardActions:
        return CardActions(
            make_default=self.make_default,
            check=self.check,
            login=self.login,
            try_connection=self.try_connection,
            delete_key=self.delete_key,
            set_model=self.set_model,
            set_base_url=self.set_base_url,
            save_key=self.save_key,
            allow_tool_agent=self.allow_tool_agent,
            pull_model=self.pull_model,
        )

    def attach(self, view: ConnectionsView) -> None:
        self.view = view
        self.render()

    # --- Görünüm ------------------------------------------------------------------------

    def render(self) -> None:
        """Kartları güncel ayarlarla doldurur (durum yoklamalarına dokunmaz)."""
        if self.view is None:
            return
        providers = self.app.settings.providers
        default = self.app.provider_name()
        for info in PROVIDERS:
            card = self.view.cards[info.name]
            cfg = getattr(providers, info.name)
            choices = [*self.discovered.get(info.name, []), *self.suggestions.get(info.name, [])]
            card.set_model(cfg.model, choices)
            card.set_default(info.name == default)
            if info.kind == "api":
                card.set_key_source(
                    key_source(providers, info.name, self.vaulted), key_env(providers, info.name)
                )
            elif info.kind == "local":
                card.set_base_url(cfg.base_url)
            elif info.name in TOOL_AGENTS:
                card.set_tool_agent(bool(cfg.allow_tool_agent))
            if info.name in self.probes:
                card.set_probe(self.probes[info.name])

    def _card_message(self, name: str, text: str, ok: bool) -> None:
        if self.view is not None:
            self.view.cards[name].set_message(text, ok)

    # --- Yoklamalar ---------------------------------------------------------------------

    def refresh_all(self) -> None:
        for info in PROVIDERS:
            self.check(info.name)
        settings = self.app.settings
        self.app.bridge.submit("compilers", lambda _emit: compiler_statuses(settings))

    def check(self, name: str) -> None:
        settings = self.app.settings
        self.probes.pop(name, None)
        if self.view is not None:
            self.view.cards[name].set_probe(None)
        if name == self.app.provider_name():
            self.app.sidebar.set_provider(name, None)
        self.app.bridge.submit(f"probe:{name}", lambda _emit: asyncio.run(probe(name, settings)))

    def handle(self, message: Message) -> None:
        kind, _, name = message.task.partition(":")
        if kind == "compilers":
            if message.kind == "result" and self.view is not None:
                compilers = cast(list[CompilerStatus], message.payload)  # bridge yükü Any
                settings = self.app.settings
                self.view.show_compilers(
                    compilers,
                    offer_download=offer_compiler_download(settings, compilers),
                    update_available=compiler_update_available(settings),
                )
        elif kind == "toolchain":
            self._on_toolchain(message)
        elif kind == "probe":
            self._on_probe(name, message)
        elif kind == "test" and message.kind != "event":
            text = str(message.payload)
            self._card_message(name, text, message.kind == "result" and text.startswith("Bağlantı"))
        elif kind == "pull" and message.kind != "event":
            self._on_pull(name, message)

    def _on_probe(self, name: str, message: Message) -> None:
        if message.kind == "result" and isinstance(message.payload, Probe):
            result = message.payload
        else:
            result = Probe(
                ProviderStatus(name=name, model="—", ready=False, detail=str(message.payload))
            )
        self.probes[name] = result
        if result.models:
            self.discovered[name] = result.models
        if name == self.app.provider_name():
            self.app.sidebar.set_provider(name, result.ready, result.status.model or "")
        self.render()

    # --- Ollama model indirme (Faz F, F10) -----------------------------------------------

    @property
    def is_pulling(self) -> bool:
        """En az bir `ollama pull` indirmesi sürüyor mu."""
        return bool(self._pull_cancellations)

    def pull_model(self, name: str) -> None:
        """Seçili modeli `ollama pull` ile indirir; doğrulama anında, indirme arka planda.

        Model adı güvensizse ya da `ollama` PATH'te yoksa hiçbir süreç başlatılmaz; kullanıcı
        Türkçe uyarı görür. Gerçek `ollama` yalnız kullanıcı isterse çalışır (testler bunu
        taklit eder).
        """
        model = getattr(self.app.settings.providers, name).model
        try:
            argv = ollama_pull_argv(model, os.environ.get("PATH", ""))
        except OllamaPullError as exc:
            self._card_message(name, str(exc), False)
            self.app.toast(str(exc))
            return
        cancellation = Cancellation()
        self._pull_cancellations[name] = cancellation
        self._card_message(name, f"{model} indiriliyor… (bu birkaç dakika sürebilir)", True)

        def _pull(_emit: Emit) -> PullOutcome:
            try:
                return run_ollama_pull(model, argv, cancel=cancellation.event)
            except TypeError:
                return run_ollama_pull(model, argv)

        self.app.bridge.submit(
            f"pull:{name}",
            _pull,
            cancellation=cancellation,
        )

    def cancel_pull(self, name: str) -> None:
        """Süren model indirmesini iptal eder."""
        cancellation = self._pull_cancellations.pop(name, None)
        if cancellation is not None:
            cancellation.cancel()
        self.app.bridge.cancel(f"pull:{name}")

    def _on_pull(self, name: str, message: Message) -> None:
        self._pull_cancellations.pop(name, None)
        if message.kind == "result" and isinstance(message.payload, PullOutcome):
            outcome = message.payload
        else:  # köprü istisnayı metne çevirdi
            outcome = PullOutcome(False, str(message.payload))
        self._card_message(name, outcome.message, outcome.ok)
        self.app.toast(outcome.message)

    # --- Derleyici indirme (Faz 29) ------------------------------------------------------

    def download_compiler(self) -> None:
        """Zig'i arka planda indirir; ilerleme `toolchain` görevi olaylarıyla gelir."""
        if self.app.bridge.is_running("toolchain"):  # iptal edilen indirme henüz kapanıyor
            self.app.toast("Önceki indirme kapanıyor; birkaç saniye sonra yeniden dene.")
            return
        settings = self.app.settings.validation
        cancellation = Cancellation()
        self.download_cancellation = cancellation

        def work(emit: Emit) -> str | None:
            try:
                return str(install_zig(settings, progress=emit, cancel=cancellation.event))
            except InstallCancelledError:
                return None  # yarım dosyalar install_zig içinde silindi

        if self.view is not None:
            self.view.set_download_running("İndirme başlatılıyor…", None)
        self.app.bridge.submit("toolchain", work, cancellation=cancellation)

    def cancel_download(self) -> None:
        """İşçiye iptal işareti verir; sonuç (iptal ya da son anda tamamlanma) işçiden gelir."""
        if self.download_cancellation is None:
            return
        self.download_cancellation.cancel()
        if self.view is not None:
            self.view.set_download_cancelling()

    def _on_toolchain(self, message: Message) -> None:
        if self.view is None:
            return
        if message.kind == "event" and isinstance(message.payload, DownloadProgress):
            self.view.set_download_running(*describe_progress(message.payload))
        elif message.kind == "result" and message.payload is None:
            self.download_cancellation = None
            self.view.set_download_idle(
                "İndirme iptal edildi; yarım kalan dosyalar silindi.", ok=True, offer=True
            )
        elif message.kind == "result":
            self.download_cancellation = None
            clear_toolchain_cache()
            self.view.set_download_idle(
                "Derleyici kuruldu; C/C++/Unreal kodu artık derleyiciyle de denetlenir.",
                ok=True,
                offer=False,
            )
            self.app.toast("Derleyici (zig) kuruldu")
            settings = self.app.settings
            self.app.bridge.submit("compilers", lambda _emit: compiler_statuses(settings))
        elif message.kind == "error":
            self.download_cancellation = None
            self.view.set_download_idle(str(message.payload), ok=False, offer=True)

    # --- Eylemler -----------------------------------------------------------------------

    def make_default(self, name: str) -> None:
        self.app.save_prefs(provider=None if name == self.app.base_default() else name)
        self.app.toast(f"Varsayılan sağlayıcı: {INFO[name].label if name in INFO else name}")
        self.render()
        self.app.sidebar.set_provider(name, None, self.app.current_model())
        self.check(name)

    def _override(self, name: str, **changes: Any) -> None:
        current = self.app.prefs.providers.get(name, ProviderOverride())
        updated = {**self.app.prefs.providers, name: current.model_copy(update=changes)}
        self.app.save_prefs(providers=updated)
        self.app.apply_settings()
        self.render()
        self.check(name)

    def set_model(self, name: str, model: str) -> None:
        model = model.strip()
        if model and model != getattr(self.app.settings.providers, name).model:
            self._override(name, model=model)

    def set_base_url(self, name: str, url: str) -> None:
        if url and not url.startswith(("http://", "https://")):
            self._card_message(name, "Adres http:// ya da https:// ile başlamalı.", False)
            return
        self._override(name, base_url=url or None)

    def allow_tool_agent(self, name: str, allowed: bool) -> None:
        self._override(name, allow_tool_agent=allowed)

    def save_key(self, name: str, key: str) -> None:
        try:
            self.store.set(name, key)
        except KeyStoreError as exc:
            self._card_message(name, str(exc), False)
            return
        apply_key(self.app.settings.providers, name, key)
        self.vaulted.add(name)
        self.app.toast(f"{INFO[name].label} anahtarı kimlik kasasına kaydedildi")
        self.render()
        self.check(name)

    def delete_key(self, name: str) -> None:
        try:
            self.store.delete(name)
        except KeyStoreError as exc:
            self._card_message(name, str(exc), False)
            return
        if name in self.vaulted:
            apply_key(self.app.settings.providers, name, None)
            self.vaulted.discard(name)
        self.render()
        self.check(name)

    def purge_legacy_keys(self) -> None:
        """ADR-0021: kaldırılan sağlayıcıların kasadaki kalıntı anahtarlarını temizler (F8)."""
        try:
            removed = self.store.purge_legacy()
        except KeyStoreError as exc:
            self.app.toast(str(exc))
            return
        if removed:
            self.app.toast(f"{removed} eski anahtar kimlik kasasından silindi")
        else:
            self.app.toast("Silinecek eski anahtar bulunamadı")

    def login(self, name: str) -> None:
        """CLI oturum açma penceresini açar; terminal yoksa komutu bildirimle söyler (F12)."""
        try:
            open_login_console(name, self.app.settings.providers)
        except LoginUnavailableError as exc:
            self.app.toast(str(exc).removeprefix(f"{name}: "))
            return
        except (ProviderError, OSError) as exc:
            self._card_message(name, f"Oturum açma başlatılamadı: {exc}", False)
            return
        self._card_message(
            name, "Açılan pencerede oturum aç, sonra bu kartta Denetle'ye bas.", True
        )

    def try_connection(self, name: str) -> None:
        settings = self.app.settings
        self._card_message(name, "Küçük bir deneme isteği gönderiliyor…", True)
        self.app.bridge.submit(
            f"test:{name}", lambda _emit: asyncio.run(try_connection(name, settings))
        )
