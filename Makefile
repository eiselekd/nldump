TARGETS += nltrace
TARGETS += preload.so

all: $(TARGETS)

CFLAGS += -D_GNU_SOURCE -Wall -Wextra -I/usr/include/libnl3 -g -fPIC
LFLAGS += -lnl-3
LFLAGS += -lnl-route-3
LFLAGS += -lnl-genl-3
LFLAGS += -lnl-nf-3

.c.o:
	$(CC) $(CFLAGS) -c $< -o $@

COMMON_SRC += process.o
COMMON_SRC += nl_stub.o
COMMON_SRC += handlers.o
COMMON_SRC += descriptor.o

NLTRACE_SRC = $(COMMON_SRC)
NLTRACE_SRC += main.o
NLTRACE_SRC += syscalls.o
NLTRACE_SRC += tracer.o

PRELOAD_LFLAGS = $(LFLAGS)
PRELOAD_LFLAGS += -ldl -shared
PRELOAD_SRC = $(COMMON_SRC)
PRELOAD_SRC += ldpreload.o


nltrace: $(NLTRACE_SRC)
	$(CC) $(NLTRACE_SRC) $(LFLAGS) -o $@

preload.so: $(PRELOAD_SRC)
	$(CC) $(PRELOAD_SRC) $(PRELOAD_LFLAGS) -o $@

indent:
	indent *.c *.h

clean:
	rm -f *.[oais] *~ $(TARGETS)


#############################

strace:
	cd strace-4.15; DEB_BUILD_OPTIONS=nocheck dpkg-buildpackage -us -uc -nc

libnl:
	cd libnl3-3.2.29/; \
		CFLAGS="-g -O2 " \
		CXXFLAGS="-g -O2 " \
		CPPFLAGS="-Wdate-time " \
		LDFLAGS="-Wl,-Bsymbolic-functions -Wl,-z,relro" \
			./configure --disable-dynamic --enable-static --build=x86_64-linux-gnu --prefix=$(CURDIR)/bin-libnl/ --includedir="$(CURDIR)/bin-libnl/include" --mandir="$(CURDIR)/bin-libnl/share/man" --infodir="$(CURDIR)/bin-libnl/share/info" --sysconfdir=$(CURDIR)/bin-libnl//etc --localstatedir=$(CURDIR)/bin-libnl//var --libexecdir="$(CURDIR)/bin-libnl/lib/libnl3" --disable-maintainer-mode --disable-dependency-tracking --disable-silent-rules --libdir=$(CURDIR)/bin-libnl/lib/x86_64-linux-gnu; make; make install
	mkdir -p lib
	cp bin-libnl/lib/x86_64-linux-gnu/*.a lib/


hostapd:
	cp wpa-2.4/debian/config/hostapd/linux wpa-2.4/hostapd/.config
	cd wpa-2.4/hostapd; make V=1 LDFLAGS="-L$(CURDIR)/lib "


hostapd-clean:
	cd wpa-2.4/hostapd; make clean
