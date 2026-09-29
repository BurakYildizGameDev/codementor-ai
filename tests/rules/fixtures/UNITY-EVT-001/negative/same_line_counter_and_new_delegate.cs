using System;
using UnityEngine;

public class Counter : MonoBehaviour
{
    public event Action Tick;
    public event Action Reset;
    int count;
    void OnEnable() { Tick += OnTick; count += 1; Reset += new Action(OnReset); }
    void OnDisable() { Tick -= OnTick; Reset -= OnReset; }
    void OnTick() { }
    void OnReset() { }
}
