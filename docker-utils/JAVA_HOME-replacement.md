Replace line with containing initialisation of JAVA_MAJOR_VERSION with below line

JAVA_MAJOR_VERSION=$($JAVA -version 2>&1 | sed -E -n 's/.* version "([^.-]*).*/\1/p')
