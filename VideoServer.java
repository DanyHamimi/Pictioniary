import java.io.*;
import java.net.*;
import java.util.concurrent.*;

public class VideoServer {
    private static final int PORT = 8080;
    private static final int MAX_GAMES = 5;
    private static final int MAX_PLAYERS_PER_GAME = 2;

    private static final ConcurrentHashMap<Integer, Game> games = new ConcurrentHashMap<>();

    public static void main(String[] args) throws IOException {
        for (int i = 0; i < MAX_GAMES; i++) {
            games.put(i, new Game());
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

    static class Game {
        ConcurrentHashMap<Socket, DataOutputStream> clients = new ConcurrentHashMap<>();
        int valToFind = -1;
        ConcurrentHashMap<Socket, Integer> scores = new ConcurrentHashMap<>();

        public void updateValToFind() {
            this.valToFind = (int) (Math.random() * 10);
            System.out.println("Nouvelle valeur à trouver: " + valToFind + "Dans la partie " + games.values().stream().filter(g -> g.clients.containsValue(clients.values().toArray()[0])).findFirst().get());
            //Send to all clients the new value to find with a blank image and a score of 0
            
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
                Game game = games.get(servIndexUser);

                if (game.clients.size() < MAX_PLAYERS_PER_GAME) {
                    DataOutputStream outputStream = new DataOutputStream(clientSocket.getOutputStream());
                    game.clients.put(clientSocket, outputStream);
                    game.scores.put(clientSocket, 0);
                    System.out.println("Client " + clientSocket.getRemoteSocketAddress() + " ajouté à la partie " + servIndexUser);

                    if (game.clients.size() == MAX_PLAYERS_PER_GAME) {
                        game.updateValToFind();
                        for (DataOutputStream out : game.clients.values()) {
                            out.writeUTF("NEW_VAL_TO_FIND " + game.valToFind);
                        }
                    }
                } else {
                    throw new IOException("Partie pleine");
                }

                while (true) {
                    int score = inputStream.readInt();
                    int length = inputStream.readInt();
                    if (length > 0) {
                        byte[] image = new byte[length];
                        inputStream.readFully(image, 0, length);

                        if (game.scores.get(clientSocket) != score) {
                            game.scores.put(clientSocket, score);
                            game.updateValToFind();
                            for (DataOutputStream out : game.clients.values()) {
                                out.writeUTF("NEW_VAL_TO_FIND " + game.valToFind);
                            }
                        }

                        game.clients.entrySet().stream()
                                .filter(entry -> entry.getKey() != clientSocket)
                                .forEach(entry -> {
                                    try {
                                        entry.getValue().writeInt(game.valToFind);
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
                e.printStackTrace();
            } finally {
                Game game = games.values().stream().filter(g -> g.clients.containsKey(clientSocket)).findFirst().orElse(null);

        if (game != null) {
            game.clients.remove(clientSocket);
            game.scores.remove(clientSocket);
        }

        try {
            clientSocket.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
    }
}

