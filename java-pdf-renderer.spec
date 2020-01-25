#
# Conditional build:
%bcond_without	javadoc		# don't build javadoc

%define		rel	1
%define		svn_date 20110310
%define		svn_version 128svn
%define		alternate_name PDFRenderer
%define		srcname		pdf-renderer
Summary:	A 100% Java PDF renderer and viewer
Name:		java-%{srcname}
Version:	0
Release:	0.%{svn_version}.%{svn_date}.%{rel}
License:	LGPL v2+
Group:		Libraries/Java
URL:		https://pdf-renderer.dev.java.net/
Source0:	%{srcname}-%{svn_version}-%{svn_date}.tar.bz2
# Source0-md5:  f46cdc9f014e3ec9d47704e46b249209
# To fetch the source code
Source1:	get-source.sh
BuildRequires:	ant
BuildRequires:	ant-apache-regexp
BuildRequires:	fonts-Type1-urw
BuildRequires:	jdk >= 1.6
BuildRequires:	jpackage-utils
Requires:	fonts-Type1-urw
Requires:	jpackage-utils >= 1.5
Obsoletes:	pdf-renderer
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The PDF Renderer is just what the name implies: an open source, all
Java library which renders PDF documents to the screen using Java2D.
Typically this means drawing into a Swing panel, but it could also
draw to other Graphics2D implementations. It could be used to draw on
top of PDFs, share them over a network, convert PDFs to PNG images, or
maybe even project PDFs into a 3D scene.

%package javadoc
Summary:	Javadoc for PDF Renderer
Group:		Documentation
Requires:	jpackage-utils

%description javadoc
API documentation for the PDF Renderer package.

%package demo
Summary:	Demo for PDF Renderer
Summary(pl.UTF-8):	Pliki demonstracyjne dla pakietu PDF Renderer
Group:		Documentation
Requires:	%{name} = %{version}-%{release}

%description demo
Demonstrations and samples for PDF Renderer.

%description demo -l pl.UTF-8
Pliki demonstracyjne i przykłady dla pakietu PDF Renderer.

%prep
%setup -q -n %{srcname}-%{svn_version}-%{svn_date}

# Remove preshipped binaries
find -name "*.jar" | xargs -r rm -v
# Remove preshipped fonts
find -name "*.pfb" | xargs -r rm -v

# Fix encoding issues
find -name "*.java" -exec native2ascii {} {} \;

# tell the program to use system-fonts
# Script provided by Mamoru Tasaka:
# https://bugzilla.redhat.com/show_bug.cgi?id=466394#c4
# -------------------------------------------------------------
cd src/com/sun/pdfview/font/res
INPUT=BaseFonts.properties
OUTPUT=BaseFonts.properties.1
FONTDIR=%{_datadir}/fonts/default/Type1

rm -f $OUTPUT
cat $INPUT | while read line; do
	newline=$line
	if echo $newline | grep -q 'file=.*pfb'; then
		pfbname=$(echo $newline | sed -e 's|^.*file=||')
		newline=$(echo $newline | sed -e "s|file=|file=${FONTDIR}/|")
	elif echo $newline | grep -q 'length='
		then
		size=$(ls -al ${FONTDIR}/$pfbname | awk '{print $5}')
		newline=$(echo $newline | sed -e "s|length=.*|length=$size|")
	fi
	echo $newline >> $OUTPUT
done
mv -f $OUTPUT $INPUT
cd -

%build
%ant

%install
rm -rf $RPM_BUILD_ROOT
# jars
install -d $RPM_BUILD_ROOT%{_javadir}
cp -p dist/%{alternate_name}.jar $RPM_BUILD_ROOT%{_javadir}/%{srcname}-%{version}.jar
ln -s %{srcname}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{srcname}.jar

# javadoc
%if %{with javadoc}
install -d $RPM_BUILD_ROOT%{_javadocdir}/%{srcname}-%{version}
cp -a dist/javadoc/* $RPM_BUILD_ROOT%{_javadocdir}/%{srcname}-%{version}
ln -s %{srcname}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{srcname} # ghost symlink
%endif

# demo
install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -a demos/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%post javadoc
ln -nfs %{srcname}-%{version} %{_javadocdir}/%{srcname}

%files
%defattr(644,root,root,755)
%{_javadir}/%{srcname}-%{version}.jar
%{_javadir}/%{srcname}.jar

%if %{with javadoc}
%files javadoc
%defattr(644,root,root,755)
%{_javadocdir}/%{srcname}-%{version}
%ghost %{_javadocdir}/%{srcname}
%endif

%files demo
%defattr(644,root,root,755)
%{_examplesdir}/%{name}-%{version}
