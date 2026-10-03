// EXPECT: 8
using UnityEngine;

public class Mover : MonoBehaviour
{
    void Update()
    {
        var rb = GetComponent<Rigidbody>();
        rb.WakeUp();
    }
}

// Faz 32: aynı adlı ama tabansız sınıfın Update'i motor tarafından çağrılmaz, sıcak değil
public class Planner
{
    public void Update(GameObject go)
    {
        var rb = go.GetComponent<Rigidbody>();
        rb.Sleep();
    }
}
