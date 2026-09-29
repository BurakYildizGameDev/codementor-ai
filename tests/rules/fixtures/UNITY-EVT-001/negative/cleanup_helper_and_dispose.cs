using System;
using UnityEngine;

public class Hud : MonoBehaviour
{
    public static event Action Changed;
    void OnEnable() { Changed += Refresh; }
    void OnDisable() { Unsubscribe(); }
    void Unsubscribe() { Changed -= Refresh; }
    void Refresh() { }
}

public class Watcher : IDisposable
{
    public Watcher() { Hud.Changed += OnChanged; }
    public void Dispose() { Hud.Changed -= OnChanged; }
    void OnChanged() { }
}
