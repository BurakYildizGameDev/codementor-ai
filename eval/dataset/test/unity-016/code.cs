using UnityEngine;

public class TargetMarker : MonoBehaviour
{
    public Transform target;

    private void LateUpdate()
    {
        Vector3? position = target?.position;
        if (position.HasValue)
        {
            transform.position = position.Value + Vector3.up * 2f;
        }
    }
}
