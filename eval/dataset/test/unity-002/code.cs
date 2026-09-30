using UnityEngine;

public class Spinner : MonoBehaviour
{
    public float degreesPerSecond = 90f;

    private void Update()
    {
        transform.Rotate(0f, degreesPerSecond * Time.deltaTime, 0f);

    private void OnDisable()
    {
        transform.rotation = Quaternion.identity;
    }
}
