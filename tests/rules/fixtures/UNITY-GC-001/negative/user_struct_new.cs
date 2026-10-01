using UnityEngine;

public struct Hit
{
    public int Damage;
    public Hit(int damage) { Damage = damage; }
}

public class Shooter : MonoBehaviour
{
    void Update()
    {
        // Hit dosyada bildirilen bir struct: `new` yığında değer oluşturur, heap tahsisi değil
        var hit = new Hit(3);
        Debug.Log(hit.Damage);
    }
}
