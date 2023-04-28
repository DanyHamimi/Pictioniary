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
        int valToFind = 9;
        ConcurrentHashMap<Socket, Integer> scores = new ConcurrentHashMap<>();

        public void updateValToFind() {
            this.valToFind = (int) (Math.random() * 10);
            System.out.println("Nouvelle valeur à trouver: " + valToFind + " Dans la partie " + games.values().stream().filter(g -> g.clients.containsValue(clients.values().toArray()[0])).findFirst().get());
            //Send to all clients the new value to find with a blank image and a score of 0
            
        }
    }

    static class ClientHandler implements Runnable {
        private final Socket clientSocket;
        private String username;

        public ClientHandler(Socket clientSocket) {
            this.clientSocket = clientSocket;
        }

        @Override
        public void run() {
            try {
                DataInputStream inputStream = new DataInputStream(clientSocket.getInputStream());
                DataOutputStream outputStream = new DataOutputStream(clientSocket.getOutputStream());
                BufferedReader inputReader = new BufferedReader(new InputStreamReader(clientSocket.getInputStream()));
                PrintWriter outputWriter = new PrintWriter(clientSocket.getOutputStream(), true);

                String receivedMessage = inputReader.readLine();
                System.out.println("Received message: " + receivedMessage);

                // Si le message est "defaultUser", renvoyez "salut" et terminez le thread
                if ("hello".equalsIgnoreCase(receivedMessage)) {
                    //Print all the games and their number of players
                    String gamesString = "";
                    for (int i = 0; i < MAX_GAMES; i++) {
                        gamesString += "Partie " + i + " : " + games.get(i).clients.size() + "/" + MAX_PLAYERS_PER_GAME + ";";
                    }
                    outputWriter.println(gamesString);
                    clientSocket.close();
                }
                else{
                    username = receivedMessage;
                }

                int servIndexUser = inputStream.readInt();
                Game game = games.get(servIndexUser);

                if (game.clients.size() < MAX_PLAYERS_PER_GAME) {
                    game.clients.put(clientSocket, outputStream);
                    game.scores.put(clientSocket, 0);
                    System.out.println("Client " + clientSocket.getRemoteSocketAddress() + " ajouté à la partie " + servIndexUser);

                    if (game.clients.size() > 0) {
                        game.updateValToFind();
                        for (DataOutputStream out : game.clients.values()) {
                            out.writeInt(-2000);
                            System.out.print("ENVOYE1");
                            out.writeInt(game.valToFind);
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
                                out.writeInt(-2000);
                                System.out.print("ENVOYE2");
                                out.writeInt(game.valToFind);
                            }
                        }

                        game.clients.entrySet().stream()
                                .filter(entry -> entry.getKey() != clientSocket)
                                .forEach(entry -> {
                                    try {
                                        entry.getValue().writeInt(2);
                                        entry.getValue().writeInt(score);
                                        entry.getValue().writeInt(length);
                                        entry.getValue().write(image);
                                        entry.getValue().writeUTF(username); // Ajout de l'username
                                        System.out.print("ENVOYE3");
                                    } catch (IOException e) {
                                        System.out.println("ERREUR LORS DE L'ENVOI DU MESSAGE");
                                        e.printStackTrace();
                                    }
                                });
                    }
                }
            } catch (IOException e) {
                //Print that user left 
                System.out.println("Client " + clientSocket.getRemoteSocketAddress() + " s'est déconnecté");
                //e.printStackTrace();
            } finally {
                Game game = games.values().stream().filter(g -> g.clients.containsKey(clientSocket)).findFirst().orElse(null);

                if (game != null) {
                    game.clients.remove(clientSocket);
                    game.scores.remove(clientSocket);
                }

                try {
                    clientSocket.close();
                } catch (IOException e) {
                    System.out.println("ERREUR LORS FERMETURE SOCKET");
                    e.printStackTrace();
                }
            }
        }
    }
}

