FROM mottosso/mayabase-centos

MAINTAINER marcus@abstractfactory.io

# Download and unpack distribution first, Docker's caching
# mechanism will ensure that this only happens once.
RUN wget https://edutrial.autodesk.com/NET18SWDLD/2018/MAYA/ESD/Autodesk_Maya_2018_EN_Linux_64bit.tgz -O maya.tgz && \
    mkdir /maya && tar -xvf maya.tgz -C /maya && \
    rm maya.tgz && \
    rpm -Uvh /maya/Maya*.rpm && \
    rm -r /maya

# Make mayapy the default Python
RUN echo alias hpython="\"/usr/autodesk/maya/bin/mayapy\"" >> ~/.bashrc && \
    echo alias hpip="\"mayapy -m pip\"" >> ~/.bashrc

# Setup environment
ENV MAYA_LOCATION=/usr/autodesk/maya/
ENV PATH=$MAYA_LOCATION/bin:$PATH

# Workaround for "Segmentation fault (core dumped)"
# See https://forums.autodesk.com/t5/maya-general/render-crash-on-linux/m-p/5608552/highlight/true
ENV MAYA_DISABLE_CIP=1

# Cleanup
WORKDIR /root

# ここにHoudini と Blender を作りたい

----


FROM mottosso/maya:2016sp1

RUN wget https://bootstrap.pypa.io/get-pip.py && \
	mayapy get-pip.py && \
	mayapy -m pip install \
		nose \
		nose-exclude \
		coverage \
		sphinx \
		six \
		sphinxcontrib-napoleon \
		python-coveralls

# Support building of Maya plug-ins
RUN yum groupinstall -y 'Development Tools' && \
	yum install -y scons

RUN git clone https://github.com/autodesk-adn/Maya-devkit.git /devkit && \
	rm -rf /usr/autodesk/maya/devkit \
		   /usr/autodesk/maya/mkspecs \
		   /usr/autodesk/maya/include && \
	ln -s /devkit/linux/devkit /usr/autodesk/maya/devkit && \
	ln -s /devkit/linux/mkspecs /usr/autodesk/maya/mkspecs && \
	ln -s /devkit/linux/include /usr/autodesk/maya/include

# Avoid creation of auxilliary files
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /workspace

ENTRYPOINT \
	scons no-cache=1 with-maya=2016 with-mayadevkit=/usr/autodesk/maya/devkit && \
	mayapy -u run_tests.py