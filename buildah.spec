# Copyright 2025 Wong Hoi Sing Edison <hswong3i@pantarei-design.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

%global debug_package %{nil}

%global source_date_epoch_from_changelog 0

Name: buildah
Epoch: 100
Version: 1.41.3
Release: 1%{?dist}
Summary: Container image repository tool
License: Apache-2.0
URL: https://github.com/containers/buildah/tags
Source0: %{name}_%{version}.orig.tar.gz
%if 0%{?rhel} == 7
BuildRequires: devtoolset-11
BuildRequires: devtoolset-11-gcc
BuildRequires: devtoolset-11-gcc-c++
BuildRequires: devtoolset-11-libatomic-devel
%endif
BuildRequires: golang-1.25
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
%setup -T -c -n %{name}_%{version}-%{release}
tar -zx -f %{S:0} --strip-components=1 -C .
%autopatch -p1

%build
%if 0%{?rhel} == 7
. /opt/rh/devtoolset-11/enable
%endif
mkdir -p bin
set -ex && \
    export CGO_ENABLED=1 && \
    go build \
        -mod vendor -buildmode pie -v \
        -ldflags "-s -w" \
        -tags "netgo osusergo exclude_graphdriver_devicemapper exclude_graphdriver_btrfs containers_image_openpgp seccomp systemd selinux" \
        -o ./bin/buildah ./cmd/buildah

%install
install -Dpm755 -d %{buildroot}%{_bindir}
install -Dpm755 -d %{buildroot}%{_prefix}/share/bash-completion/completions
install -Dpm755 -t %{buildroot}%{_bindir}/ bin/buildah
install -Dpm644 -t %{buildroot}%{_prefix}/share/bash-completion/completions contrib/completions/bash/buildah

%files
%license LICENSE
%{_bindir}/*
%{_prefix}/share/bash-completion/completions/*

%changelog

