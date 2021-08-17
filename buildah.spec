%global debug_package %{nil}

Name: buildah
Epoch: 100
Version: 1.22.4
Release: 1%{?dist}
Summary: Container image repository tool
License: Apache-2.0
URL: https://github.com/containers/buildah/tags
Source0: %{name}_%{version}.orig.tar.gz
BuildRequires: golang-1.17
BuildRequires: glibc-static
BuildRequires: glib2-devel
BuildRequires: gpgme-devel
BuildRequires: libassuan-devel
BuildRequires: libgpg-error-devel
BuildRequires: libseccomp-devel
BuildRequires: libselinux-devel
BuildRequires: make
BuildRequires: pkgconfig
BuildRequires: systemd-devel
Requires: containers-common
Requires: iptables
Requires: libassuan.so.0()(64bit)
Requires: libglib-2.0.so.0()(64bit)
Requires: libgpg-error.so.0()(64bit)
Requires: libgpgme.so.11()(64bit)
Requires: libseccomp.so.2()(64bit)
Requires: libselinux.so.1()(64bit)
Requires: libsystemd.so.0()(64bit)
Requires: oci-runtime

%description
Buildah provides a command line tool which can be used to:
  - Create a working container, either from scratch or using an image as
    a starting point
  - Create an image, either from a working container or via the
    instructions in a Dockerfile
  - Build images in either the OCI image format or the traditional
    upstream docker image format
  - Mount a working container's root filesystem for manipulation
  - Unmount a working container's root filesystem
  - Update the contents of a container's root filesystem
  - Delete a working container or an image

%prep
%autosetup -T -c -n %{name}_%{version}-%{release}
tar -zx -f %{S:0} --strip-components=1 -C .

%build
mkdir -p bin
set -ex && \
    export CGO_ENABLED=1 && \
    go build \
        -mod vendor -buildmode pie -v \
        -ldflags "-s -w" \
        -tags "netgo osusergo exclude_graphdriver_devicemapper exclude_graphdriver_btrfs containers_image_openpgp seccomp selinux" \
        -o ./bin/buildah ./cmd/buildah

%install
install -Dpm755 -d %{buildroot}%{_bindir}
install -Dpm755 -d %{buildroot}%{_prefix}/share/bash-completion/completions
install -Dpm755 -t %{buildroot}%{_bindir}/ bin/buildah
install -Dpm644 -t %{buildroot}%{_prefix}/share/bash-completion/completions contrib/completions/bash/buildah

%files
%license LICENSE
%{_bindir}/buildah
%{_prefix}/share/bash-completion/completions/buildah

%changelog

