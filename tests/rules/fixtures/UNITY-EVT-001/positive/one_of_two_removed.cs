// EXPECT: 11
using System;
using UnityEngine;

public class Player : MonoBehaviour
{
    public event Action Died;
    void OnEnable()
    {
        Died += PlaySound;
        Died += ShowScreen;
    }
    void OnDisable()
    {
        Died -= PlaySound;
    }
    void PlaySound() { }
    void ShowScreen() { }
}
