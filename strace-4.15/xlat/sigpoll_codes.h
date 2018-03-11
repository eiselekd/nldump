/* Generated by ../xlat/gen.sh from ../xlat/sigpoll_codes.in; do not edit. */
#if !(defined(POLL_IN) || (defined(HAVE_DECL_POLL_IN) && HAVE_DECL_POLL_IN))
# define POLL_IN 1
#endif
#if !(defined(POLL_OUT) || (defined(HAVE_DECL_POLL_OUT) && HAVE_DECL_POLL_OUT))
# define POLL_OUT 2
#endif
#if !(defined(POLL_MSG) || (defined(HAVE_DECL_POLL_MSG) && HAVE_DECL_POLL_MSG))
# define POLL_MSG 3
#endif
#if !(defined(POLL_ERR) || (defined(HAVE_DECL_POLL_ERR) && HAVE_DECL_POLL_ERR))
# define POLL_ERR 4
#endif
#if !(defined(POLL_PRI) || (defined(HAVE_DECL_POLL_PRI) && HAVE_DECL_POLL_PRI))
# define POLL_PRI 5
#endif
#if !(defined(POLL_HUP) || (defined(HAVE_DECL_POLL_HUP) && HAVE_DECL_POLL_HUP))
# define POLL_HUP 6
#endif

#ifdef IN_MPERS

extern const struct xlat sigpoll_codes[];

#else

# if !(defined HAVE_M32_MPERS || defined HAVE_MX32_MPERS)
static
# endif
const struct xlat sigpoll_codes[] = {
 XLAT(POLL_IN),
 XLAT(POLL_OUT),
 XLAT(POLL_MSG),
 XLAT(POLL_ERR),
 XLAT(POLL_PRI),
 XLAT(POLL_HUP),
 XLAT_END
};

#endif /* !IN_MPERS */