using System;
using UnityEngine;

public class TriggerZone : MonoBehaviour
{
    public static event Action<string> Entered;

    private void OnTriggerEnter(Collider other)
    {
        Entered?.Invoke(other.name);
    }
}

public class ZoneLogger : MonoBehaviour
{
    private void OnEnable()
    {
        TriggerZone.Entered += OnEntered;
    }

    private void OnEntered(string who)
    {
        Debug.Log(who + " bölgeye girdi");
    }
}
