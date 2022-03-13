FROM ubuntu:21.04
LABEL maintainer="amaharja20@mail.wou.edu"
LABEL version="0.1"
RUN apt-get update 
RUN apt-get install -y bsdmainutils
RUN mkdir ~/datashell
COPY /elements /datashell/elements
CMD ls && ... && /bin/bash
ENTRYPOINT [ "/bin/bash", "-c", "/datashell/elements/readxml.sh & sleep 5 && tail -F /dev/null"] 

