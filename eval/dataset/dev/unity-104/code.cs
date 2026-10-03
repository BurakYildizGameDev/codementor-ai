using UnityEngine;

public class PlayerController : MonoBehaviour {
    [SerializeField] private float speed = 5f;
    private Rigidbody rb;

    void Awake() {
        rb = GetComponent<Rigidbody>();
    }

    void FixedUpdate() {
        if (rb != null) {
            Vector3 movement = new Vector3(Input.GetAxis("Horizontal"), 0, Input.GetAxis("Vertical"));
            rb.velocity = movement * speed;
        }
    }

    void OnTriggerEnter(Collider other) {
        if (other.CompareTag("Coin")) {
            Destroy(other.gameObject);
        }
    }
}
