from distutils.core import setup

files = ["pylvs/*"]

execfile("pylvs/__init__.py")

setup(
    name = __pkgname__,
    version = __version__,
    description = "small wrapper to control Linux Virtual Server via ipvsadm command line client",
    author = "schlitzered",
    author_email = "schlitzered@gmail.com",
    url = "https://github.com/schlitzered/pylvs",
    packages=['pylvs'],
) 
