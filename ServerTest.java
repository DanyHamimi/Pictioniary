import java.io.*;
import java.net.*;
import java.util.concurrent.*;

public class ServerTest {
    private static final int PORT = 8080;
    private static final ConcurrentHashMap<Socket, DataOutputStream> clients = new ConcurrentHashMap<>();

    public static void main(String[] args) throws IOException {
    try (ServerSocket serverSocket = new ServerSocket(PORT)) {
        System.out.println("Serveur en attente de connexions...");

        // Utilisation d'un ExecutorService pour gérer les threads plus efficacement
        ExecutorService executorService = Executors.newCachedThreadPool();

        while (true) {
            Socket clientSocket = serverSocket.accept();
            System.out.println("Client connecté: " + clientSocket.getRemoteSocketAddress());
            DataOutputStream outputStream = new DataOutputStream(clientSocket.getOutputStream());
            clients.put(clientSocket, outputStream);
            executorService.submit(new ClientHandler(clientSocket));
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
        try (DataInputStream inputStream = new DataInputStream(clientSocket.getInputStream())) {
            while (true) {
                int length = inputStream.readInt();
                if (length > 0) {
                    byte[] image = new byte[length];
                    inputStream.readFully(image, 0, length);
                    clients.entrySet().stream()
                            .filter(entry -> entry.getKey() != clientSocket)
                            .forEach(entry -> {
                                try {
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
