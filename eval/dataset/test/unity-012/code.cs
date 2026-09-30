using System.Collections.Generic;
using UnityEngine;

public class BulletPool : MonoBehaviour
{
    [SerializeField] private Bullet prefab;
    [SerializeField] private int initialSize = 32;
    private readonly Queue<Bullet> available = new Queue<Bullet>();

    private void Awake()
    {
        for (int i = 0; i < initialSize; i++)
        {
            available.Enqueue(Create());
        }
    }

    public Bullet Get(Vector3 position, Quaternion rotation)
    {
        Bullet bullet = available.Count > 0 ? available.Dequeue() : Create();
        bullet.transform.SetPositionAndRotation(position, rotation);
        bullet.gameObject.SetActive(true);
        return bullet;
    }

    public void Release(Bullet bullet)
    {
        bullet.gameObject.SetActive(false);
        available.Enqueue(bullet);
    }

    private Bullet Create()
    {
        Bullet bullet = Instantiate(prefab, transform);
        bullet.gameObject.SetActive(false);
        return bullet;
    }
}
