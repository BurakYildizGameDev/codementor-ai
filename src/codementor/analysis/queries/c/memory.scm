; Tahsis ve serbest bırakma (mimari §5.3.1 `allocations`, `deallocations`)
((call_expression function: (identifier) @name) @alloc
  (#match? @name "^(malloc|calloc|realloc)$"))
((call_expression function: (identifier) @name) @free
  (#eq? @name "free"))
