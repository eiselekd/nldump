/* Generated by ../xlat/gen.sh from ../xlat/seccomp_filter_flags.in; do not edit. */
#if !(defined(SECCOMP_FILTER_FLAG_TSYNC) || (defined(HAVE_DECL_SECCOMP_FILTER_FLAG_TSYNC) && HAVE_DECL_SECCOMP_FILTER_FLAG_TSYNC))
# define SECCOMP_FILTER_FLAG_TSYNC 1
#endif

#ifdef IN_MPERS

# error static const struct xlat seccomp_filter_flags in mpers mode

#else

static
const struct xlat seccomp_filter_flags[] = {
 XLAT(SECCOMP_FILTER_FLAG_TSYNC),
 XLAT_END
};

#endif /* !IN_MPERS */
