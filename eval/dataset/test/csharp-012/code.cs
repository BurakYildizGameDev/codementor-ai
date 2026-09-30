using System.Collections.Generic;

public static class JobRunner
{
    public static int ProcessAll(List<int> jobs)
    {
        int done = 0;
        while (jobs.Count > 0)
        {
            int job = jobs[0];
            jobs.RemoveAt(0);
            done += job;
        }
        return done;
    }
}
