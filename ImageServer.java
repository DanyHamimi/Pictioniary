import java.io.*;
import java.net.*;
import java.util.concurrent.*;

public class ImageServer {
    private static final int PORT = 8080;
    private static final ConcurrentHashMap<Socket, DataOutputStream> clients = new ConcurrentHashMap<>();

    public static void main(String[] args) throws IOException {
        try (ServerSocket serverSocket = new ServerSocket(PORT)) {
            System.out.println("Serveur en attente de connexions...");
            while (true) {
                Socket clientSocket = serverSocket.accept();
                System.out.println("Client connecté: " + clientSocket.getRemoteSocketAddress());
                DataOutputStream outputStream = new DataOutputStream(clientSocket.getOutputStream());
                clients.put(clientSocket, outputStream);
                new Thread(new ClientHandler(clientSocket)).start();
            }
        }
    }

    static class ClientHandler implements Runnable {
        private final Socket clientSocket;

        public ClientHandler(Socket clientSocket) {
            this.clientSocket = clientSocket;
        }

        @Override
        public void run() {
            try {
                DataInputStream inputStream = new DataInputStream(clientSocket.getInputStream());
                while (true) {
                    byte[] scoreBytes = new byte[4];
                    inputStream.readFully(scoreBytes, 0, scoreBytes.length);
                    String scoreStr = new String(scoreBytes);
                    int score = Integer.parseInt(scoreStr.trim());
                    byte[] messageBytes = new byte[1024];
                    inputStream.readFully(messageBytes, 0, messageBytes.length);
                    String message = new String(messageBytes).trim();
                    int length = inputStream.readInt();
                    if (length > 0) {
                        byte[] image = new byte[length];
                        inputStream.readFully(image, 0, length);
                        clients.entrySet().stream()
                                .filter(entry -> entry.getKey() != clientSocket)
                                .forEach(entry -> {
                                    try {
                                        entry.getValue().write(scoreBytes);
                                        entry.getValue().write(messageBytes);
                                        entry.getValue().writeInt(length);
                                        entry.getValue().write(image);
                                    } catch (IOException e) {
                                        e.printStackTrace();
                                    }
                                });
                    }
                }
            } catch (IOException e) {
                e.printStackTrace();
            } finally {
                clients.remove(clientSocket);
                try {
                    clientSocket.close();
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        }             
    }
}