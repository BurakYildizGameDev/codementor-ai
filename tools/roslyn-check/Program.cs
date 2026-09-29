// CodeMentor AI — Roslyn sözdizimi denetimi (mimari §5.2.2, ADR-0009).
//
// stdin'den C# kaynağını okur, yalnızca CSharpSyntaxTree.ParseText ile ayrıştırır ve
// sözdizimi tanılarını stdout'a JSON dizisi olarak basar:
//   [{"line":1,"column":5,"severity":"error","id":"CS1002","message":"; expected"}]
// Dosya sistemine erişmez, referans derleme yüklemez, kodu derlemez veya çalıştırmaz.
// Çıkış kodu: 0 = ayrıştırma tamamlandı (tanı olsa da), 2 = araç hatası.
using System;
using System.Globalization;
using System.IO;
using System.Text;
using System.Text.Json;
using Microsoft.CodeAnalysis;
using Microsoft.CodeAnalysis.CSharp;

namespace CodeMentor.RoslynCheck;

internal static class Program
{
    private const int MaxDiagnostics = 100;

    private static int Main()
    {
        try
        {
            CultureInfo.DefaultThreadCurrentCulture = CultureInfo.InvariantCulture;
            CultureInfo.DefaultThreadCurrentUICulture = CultureInfo.InvariantCulture;

            string source;
            using (var reader = new StreamReader(Console.OpenStandardInput(), new UTF8Encoding(false)))
            {
                source = reader.ReadToEnd();
            }

            var options = new CSharpParseOptions(
                LanguageVersion.Latest, DocumentationMode.None, SourceCodeKind.Regular);
            var tree = CSharpSyntaxTree.ParseText(source, options);

            using var stdout = Console.OpenStandardOutput();
            using var json = new Utf8JsonWriter(stdout);
            json.WriteStartArray();
            var written = 0;
            foreach (var diagnostic in tree.GetDiagnostics())
            {
                if (written >= MaxDiagnostics)
                {
                    break;
                }
                var severity = diagnostic.Severity switch
                {
                    DiagnosticSeverity.Error => "error",
                    DiagnosticSeverity.Warning => "warning",
                    _ => null,
                };
                if (severity is null)
                {
                    continue;
                }
                var start = diagnostic.Location.GetLineSpan().StartLinePosition;
                json.WriteStartObject();
                json.WriteNumber("line", start.Line + 1);
                json.WriteNumber("column", start.Character + 1);
                json.WriteString("severity", severity);
                json.WriteString("id", diagnostic.Id);
                json.WriteString("message", diagnostic.GetMessage(CultureInfo.InvariantCulture));
                json.WriteEndObject();
                written++;
            }
            json.WriteEndArray();
            json.Flush();
            return 0;
        }
        catch (Exception ex)
        {
            Console.Error.WriteLine($"roslyn-check: {ex.GetType().Name}");
            return 2;
        }
    }
}
