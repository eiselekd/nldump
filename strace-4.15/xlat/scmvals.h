/* Generated by ../xlat/gen.sh from ../xlat/scmvals.in; do not edit. */
#if !(defined(SCM_RIGHTS) || (defined(HAVE_DECL_SCM_RIGHTS) && HAVE_DECL_SCM_RIGHTS))
# define SCM_RIGHTS 1
#endif
#if !(defined(SCM_CREDENTIALS) || (defined(HAVE_DECL_SCM_CREDENTIALS) && HAVE_DECL_SCM_CREDENTIALS))
# define SCM_CREDENTIALS 2
#endif
#if !(defined(SCM_SECURITY) || (defined(HAVE_DECL_SCM_SECURITY) && HAVE_DECL_SCM_SECURITY))
# define SCM_SECURITY 3
#endif

#ifdef IN_MPERS

# error static const struct xlat scmvals in mpers mode

#else

static
const struct xlat scmvals[] = {
 XLAT(SCM_RIGHTS),
 XLAT(SCM_CREDENTIALS),
 XLAT(SCM_SECURITY),
 XLAT_END
};

#endif /* !IN_MPERS */