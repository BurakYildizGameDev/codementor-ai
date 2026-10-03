using UnityEngine;

public class HazardZone : MonoBehaviour {
    void OnTriggerStay(Collider other) {
        if (other.tag == "Player") {
            Debug.Log("Player in hazard zone");
        }
    }
}
