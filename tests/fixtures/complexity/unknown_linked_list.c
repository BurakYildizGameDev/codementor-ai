// expect-hint: n | low
struct node { int value; struct node *next; };

int length(const struct node *head) {
    int n = 0;
    while (head != 0) {
        head = head->next;
        n++;
    }
    return n;
}
