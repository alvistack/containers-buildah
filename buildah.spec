%global debug_package %{nil}

Name: buildah
Epoch: 100
Version: 1.22.0
Release: 1%{?dist}
Summary: Container image repository tool
License: Apache-2.0
URL: https://github.com/containers/buildah
Source0: %{name}_%{version}.orig.tar.gz
%if 0%{?suse_version} > 1500 || 0%{?is_opensuse}
BuildRequires: go
%else
BuildRequires: golang
%endif
%if 0%{?suse_version} > 1500 || 0%{?is_opensuse}
BuildRequires: glibc-devel-static
%else
BuildRequires: glibc-static
%endif
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
Requires: glib2
Requires: gpgme
Requires: iptables
Requires: libassuan
Requires: libgpg-error
Requires: libseccomp
Requires: libselinux
Requires: oci-runtime
Requires: systemd-libs

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
CGO_ENABLED=1 \
    go build \
        -mod vendor -buildmode pie -v \
        -ldflags "-s -w" \
        -tags "netgo osusergo exclude_graphdriver_devicemapper exclude_graphdriver_btrfs containers_image_openpgp seccomp selinux" \
        -o ./bin/buildah ./cmd/buildah

%install
install -Dpm755 -d %{buildroot}%{_bindir}
install -Dpm755 -t %{buildroot}%{_bindir}/ bin/*

%files
%license LICENSE
%{_bindir}/*

%changelog

