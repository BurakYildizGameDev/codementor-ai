; Tahsis, serbest bırakma, closure ve metin birleştirme (mimari §5.3.1)
((call_expression function: (identifier) @name) @alloc
  (#match? @name "^(malloc|calloc|realloc)$"))
((call_expression function: (qualified_identifier name: (identifier) @name)) @alloc
  (#match? @name "^(malloc|calloc|realloc)$"))
((call_expression function: (qualified_identifier name: (template_function name: (identifier) @name))) @alloc
  (#match? @name "^(make_unique|make_shared)$"))
((call_expression function: (template_function name: (identifier) @name)) @alloc
  (#match? @name "^(make_unique|make_shared)$"))
((call_expression function: (identifier) @name) @free
  (#eq? @name "free"))
((call_expression function: (qualified_identifier name: (identifier) @name)) @free
  (#eq? @name "free"))
(new_expression) @new
(delete_expression) @delete
(lambda_expression) @closure
; operatör Python'da süzülür: `operator: "+"` alan deseni uzun zincirde karesel
(binary_expression) @concat
(assignment_expression) @concat_assign
