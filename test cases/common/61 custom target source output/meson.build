project('source generation', 'c')

ct = custom_target('gen',
output : ['mylib.h', 'mylib.c'],
command : [find_program('generator.py'), meson.current_build_dir()],
)

e = executable('prog', 'main.c', ct,
include_directories : include_directories('.')
)
test('gentest', e)
