import java.io.*;
import java.net.*;
import java.util.concurrent.*;

public class VideoServer {
    private static final int PORT = 8080;
    private static final int MAX_GAMES = 5;
    private static final int MAX_PLAYERS_PER_GAME = 2;

    private static final ConcurrentHashMap<Integer, ConcurrentHashMap<Socket, DataOutputStream>> gameClients = new ConcurrentHashMap<>();

    public static void main(String[] args) throws IOException {
        for (int i = 0; i < MAX_GAMES; i++) {
            gameClients.put(i, new ConcurrentHashMap<>());
        }

        try (ServerSocket serverSocket = new ServerSocket(PORT)) {
            System.out.println("Serveur en attente de connexions...");
            while (true) {
                Socket clientSocket = serverSocket.accept();
                System.out.println("Client connecté: " + clientSocket.getRemoteSocketAddress());
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
                int servIndexUser = inputStream.readInt();
                ConcurrentHashMap<Socket, DataOutputStream> clients = gameClients.get(servIndexUser);

                if (clients.size() < MAX_PLAYERS_PER_GAME) {
                    DataOutputStream outputStream = new DataOutputStream(clientSocket.getOutputStream());
                    clients.put(clientSocket, outputStream);
                    System.out.println("Client " + clientSocket.getRemoteSocketAddress() + " ajouté à la partie " + servIndexUser);
                } else {
                    throw new IOException("Partie pleine");
                }

                while (true) {
                    int score = inputStream.readInt();
                    int length = inputStream.readInt();
                    if (length > 0) {
                        byte[] image = new byte[length];
                        inputStream.readFully(image, 0, length);
                        clients.entrySet().stream()
                                .filter(entry -> entry.getKey() != clientSocket)
                                .forEach(entry -> {
                                    try {
                                        entry.getValue().writeInt(score);
                                        entry.getValue().writeInt(length);
                                        entry.getValue().write(image);
                                    } catch (IOException e) {
                                        e.printStackTrace();
                                    }
                                });
                    }
                }
            } catch (IOException e) {
                System.out.println("1");
                e.printStackTrace();
            } finally {
                for (ConcurrentHashMap<Socket, DataOutputStream> clients : gameClients.values()) {
                    clients.remove(clientSocket);
                }
                try {
                    clientSocket.close();
                } catch (IOException e) {
                    System.out.println("2");
                    e.printStackTrace();
                }
            }
        }
    }
}
