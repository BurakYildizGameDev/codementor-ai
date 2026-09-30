using UnityEngine;

public class Gun : MonoBehaviour
{
    [SerializeField] private Bullet bulletPrefab;
    [SerializeField] private Transform muzzle;
    [SerializeField] private float fireRate = 12f;
    private float nextShot;

    private void Update()
    {
        if (Input.GetButton("Fire1") && Time.time >= nextShot)
        {
            nextShot = Time.time + 1f / fireRate;
            Bullet bullet = Instantiate(bulletPrefab, muzzle.position, muzzle.rotation);
            Destroy(bullet.gameObject, 2f);
        }
    }
}
