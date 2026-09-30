using System;

public static class Clock
{
    public static event Action<int> Ticked;

    public static void Tick(int t) => Ticked?.Invoke(t);
}

public class Display
{
    private int _last;

    public Display()
    {
        Clock.Ticked += OnTicked;
    }

    private void OnTicked(int t)
    {
        _last = t;
    }
}
