using System;
using UnityEngine;

public class ZoneTrigger : MonoBehaviour
{
    public static event Action Entered;
    public static event Action Exited;

    private void OnTriggerEnter(Collider other)
    {
        if (other.CompareTag("Player")) Entered?.Invoke();
    }

    private void OnTriggerExit(Collider other)
    {
        if (other.CompareTag("Player")) Exited?.Invoke();
    }
}

public class Door : MonoBehaviour
{
    [SerializeField] private float openHeight = 2f;
    [SerializeField, Range(0.1f, 10f)] private float speed = 2f;

    private Vector3 closedPosition;
    private Vector3 target;

    private void Awake()
    {
        closedPosition = transform.position;
        target = closedPosition;
    }

    private void OnEnable()
    {
        ZoneTrigger.Entered += Open;
        ZoneTrigger.Exited += Close;
    }

    private void OnDisable()
    {
        ZoneTrigger.Entered -= Open;
        ZoneTrigger.Exited -= Close;
    }

    private void Open() => target = closedPosition + Vector3.up * openHeight;
    private void Close() => target = closedPosition;

    private void Update()
    {
        transform.position = Vector3.MoveTowards(transform.position, target, speed * Time.deltaTime);
    }
}
