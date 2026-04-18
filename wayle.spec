%global debug_package %{nil}
%define desktop_entry_filename com.wayle.settings.desktop
%bcond_without tests

Name:		wayle
Version:	0.2.1
Release:	1
Source0:	https://github.com/wayle-rs/wayle/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:	%{name}-%{version}-vendor.tar.xz
Summary:	A configurable desktop shell for Wayland compositors
URL:		https://github.com/wayle-rs/wayle
License:	MIT
Group:		Graphical desktop/Other

BuildRequires:	rust-packaging
BuildRequires:  pkgconfig(cairo)
BuildRequires:	pkgconfig(fftw3)
BuildRequires:	pkgconfig(gdk-pixbuf-2.0)
BuildRequires:	pkgconfig(gtk4)
BuildRequires:	pkgconfig(gtk4-layer-shell-0)
BuildRequires:	pkgconfig(gtksourceview-5)
BuildRequires:	pkgconfig(libpipewire-0.3)
BuildRequires:	pkgconfig(libpulse)
BuildRequires:	pkgconfig(pango)
BuildRequires:	pkgconfig(udev)
BuildRequires:	pkgconfig(xkbcommon)

Requires:	networkmanager
Requires:	bluez
Requires:	power-profiles-daemon
Requires:	matugen
Requires:	python-pywal16
Requires:	swww
Requires:	upower

%description
A configurable desktop shell for Wayland compositors.

%prep
%autosetup -p1
tar -zxf %{SOURCE1}
mkdir -p .cargo
cat >> .cargo/config.toml << EOF
[source.crates-io]
replace-with = "vendored-sources"

[source.vendored-sources]
directory = "vendor"
EOF

%build
cargo build --frozen --release

%install
install -Dm755 target/release/%{name} %{buildroot}%{_bindir}/%{name} 
install -Dm755 target/release/%{name}-settings %{buildroot}%{_bindir}/%{name}-settings

install -dm755 %{buildroot}%{_datadir}/%{name}/icons
cp -r resources/icons/hicolor %{buildroot}%{_datadir}/%{name}/icons

target/release/%{name} completions bash > %{name}.bash
target/release/%{name} completions zsh > _%{name}
target/release/%{name} completions fish > %{name}.fish

install -Dm644 %{name}.bash %{buildroot}%{_datadir}/bash-completion/completions/%{name}
install -Dm644 _%{name} %{buildroot}%{_datadir}/zsh/site-functions/_%{name}
install -Dm644 %{name}.fish %{buildroot}%{_datadir}/fish/vendor_completions.d/%{name}.fish

install -Dm644 resources/%{name}.service %{buildroot}%{_userunitdir}/%{name}.service
install -Dm644 resources/%{desktop_entry_filename} %{buildroot}%{_datadir}/applications/%{desktop_entry_filename}
install -Dm644 resources/%{name}-settings.svg %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/%{name}-settings.svg

%files
%license LICENSE
%doc README.md docs/
%{_bindir}/%{name}
%{_bindir}/%{name}-settings
%{_datadir}/%{name}/
%{_datadir}/bash-completion/completions/%{name}
%{_datadir}/zsh/site-functions/_%{name}
%{_datadir}/fish/vendor_completions.d/%{name}.fish
%{_userunitdir}/%{name}.service
%{_datadir}/applications/%{desktop_entry_filename}
%{_iconsdir}/hicolor/scalable/apps/%{name}-settings.svg
