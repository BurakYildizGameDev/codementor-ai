using UnityEngine;

public class FollowPlayer : MonoBehaviour
{
    [SerializeField] private Vector3 offset = new Vector3(0f, 5f, -8f);

    private void LateUpdate()
    {
        var player = FindObjectOfType<PlayerController>();
        transform.position = player.transform.position + offset;
    }
}
