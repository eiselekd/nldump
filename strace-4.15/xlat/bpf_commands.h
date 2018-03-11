/* Generated by ./xlat/gen.sh from ./xlat/bpf_commands.in; do not edit. */
#if !(defined(BPF_MAP_CREATE) || (defined(HAVE_DECL_BPF_MAP_CREATE) && HAVE_DECL_BPF_MAP_CREATE))
# define BPF_MAP_CREATE 0
#endif
#if !(defined(BPF_MAP_LOOKUP_ELEM) || (defined(HAVE_DECL_BPF_MAP_LOOKUP_ELEM) && HAVE_DECL_BPF_MAP_LOOKUP_ELEM))
# define BPF_MAP_LOOKUP_ELEM 1
#endif
#if !(defined(BPF_MAP_UPDATE_ELEM) || (defined(HAVE_DECL_BPF_MAP_UPDATE_ELEM) && HAVE_DECL_BPF_MAP_UPDATE_ELEM))
# define BPF_MAP_UPDATE_ELEM 2
#endif
#if !(defined(BPF_MAP_DELETE_ELEM) || (defined(HAVE_DECL_BPF_MAP_DELETE_ELEM) && HAVE_DECL_BPF_MAP_DELETE_ELEM))
# define BPF_MAP_DELETE_ELEM 3
#endif
#if !(defined(BPF_MAP_GET_NEXT_KEY) || (defined(HAVE_DECL_BPF_MAP_GET_NEXT_KEY) && HAVE_DECL_BPF_MAP_GET_NEXT_KEY))
# define BPF_MAP_GET_NEXT_KEY 4
#endif
#if !(defined(BPF_PROG_LOAD) || (defined(HAVE_DECL_BPF_PROG_LOAD) && HAVE_DECL_BPF_PROG_LOAD))
# define BPF_PROG_LOAD 5
#endif

#ifdef IN_MPERS

# error static const struct xlat bpf_commands in mpers mode

#else

static
const struct xlat bpf_commands[] = {
 XLAT(BPF_MAP_CREATE),
 XLAT(BPF_MAP_LOOKUP_ELEM),
 XLAT(BPF_MAP_UPDATE_ELEM),
 XLAT(BPF_MAP_DELETE_ELEM),
 XLAT(BPF_MAP_GET_NEXT_KEY),
 XLAT(BPF_PROG_LOAD),
 XLAT_END
};

#endif /* !IN_MPERS */