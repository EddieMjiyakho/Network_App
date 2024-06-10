# Network_App
# CSC3002 – Networks Assignment 1 – 2024
## Socket programming project

**Department of Computer Science**
**University of Cape Town, South Africa**
**February 19, 2024**

### 1. Application Description
This assignment focuses on networked applications where you will learn the basics of protocol design and socket programming with TCP and UDP connections in Python. You will develop a client-server + p2p application in groups of three students. The application to be developed is a peer-to-peer chat application that uses both UDP and TCP sockets.

### 2. Protocol Design and Specification
- Design the application to consider privacy/confidentiality by allowing users to indicate information visibility permissions.
- Define three types of messages: commands, data transfer, and control.
- Specify the structure of messages including headers and bodies.
- Define communication rules for different stages of communication.
- Include sequence diagrams.

### 3. What you need to submit
- Group server code and individual client code with proper inline documentation.
- A report (max 6 pages) on the design and functionality of your chat application (individual sections on the client implementation).
- Report should include:
  - List of features with a brief explanation for their inclusion.
  - Protocol specification detailing message formats and structure. Include sequence diagram(s).
  - Screenshots of the application revealing its features.
- Oral presentation to be scheduled with the TAs and Tutors.

### A. Multi-threaded Client/Server Applications—Sockets Programming

#### A.2. How is a network connection created?
- A client initiates a connection by creating a socket and passing the server address and port number.
- The server listens for connection requests on a specific port.
- When a connection request arrives, the server creates a new socket and binds a port to it.
- The server communicates with the client through the new port.
- TCP is connection-oriented, while UDP is connectionless and sends data in packets called datagrams.

## Writer
Sakhile Eddie Mjiyakho (MJYSAK001)
Hloni Mosikili
Ayanda Phaketsi

 
