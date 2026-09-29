using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading;
using System.Threading.Tasks;

namespace Mentor.Samples
{
    public interface IRepository<T> where T : class
    {
        Task<IReadOnlyList<T>> GetAllAsync(CancellationToken ct = default);
    }

    public sealed class MemoryRepository<T> : IRepository<T> where T : class
    {
        private readonly List<T> items = new();

        public int Count => items.Count;

        public void Add(T item) => items.Add(item ?? throw new ArgumentNullException(nameof(item)));

        public async Task<IReadOnlyList<T>> GetAllAsync(CancellationToken ct = default)
        {
            await Task.Yield();
            ct.ThrowIfCancellationRequested();
            return items.Where(i => i is not null).ToList();
        }
    }

    internal static class Program
    {
        private static async Task Main()
        {
            var repo = new MemoryRepository<string>();
            repo.Add("merhaba");
            var all = await repo.GetAllAsync();
            Console.WriteLine($"{all.Count} öğe");
        }
    }
}
