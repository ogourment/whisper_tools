from subtitle_transformer import transform_subtitles


SAMPLE_IN = """[00:00.000 --> 00:22.440]  Bienvenue dans ce vingtième et dernier épisode du Grand course à tort sur la robustesse. On va
[00:22.440 --> 00:27.120]  parler de la transformation. La question qu'on se pose c'est comment transformer,
[00:27.120 --> 00:35.120]  comment basculer de la performance à la robustesse. Pour transformer, il faut 3 ingrédients. Le
[00:35.120 --> 00:42.760]  premier c'est de l'éducation, il faut s'éduquer. Le deuxième il faut s'arrêter, il faut créer de
[00:42.760 --> 00:49.120]  l'espace pour pouvoir se transformer. Et le troisième ingrédient c'est un récit, il faut un récit pour
[00:49.120 --> 00:55.860]  mobiliser. C'est ça qu'on va explorer dans cet épisode. Je vais commencer avec les récits et
[00:55.860 --> 01:03.120]  avec ces diagrammes de la grande accélération où on voit l'impact des humains dans l'anthropocène où
[01:03.120 --> 01:08.400]  tout s'accélère depuis les années 50. Quand on voit ces courbes, elles peuvent nous faire un peu froid
[01:08.400 --> 01:13.740]  dans le dos mais on a derrière dans un coin de notre tête l'idée un petit peu de l'arrogance de
[01:13.740 --> 01:19.860]  l'humain de l'anthropocène qui se dit on a été capable de faire ça, d'avoir une dynamique exponentielle,
[01:19.860 --> 01:25.920]  de créer tous ces biens de consommation, toutes ces organisations à cet impact énorme et finalement
[01:25.920 --> 01:31.560]  il y a une forme d'attraction. C'est un peu comme le papillon qui regarde la flamme. Alors moi ce que
[01:31.560 --> 01:37.260]  je vous propose pour inverser ce récit là, c'est tout simplement d'inverser la courbe. Vraiment de
[01:37.260 --> 01:46.260]  l'inverser géométriquement et observer l'effet psychologique que ça a sur vous. De voir ces courbes
[01:46.260 --> 01:52.800]  qui maintenant tombent rapidement, d'un seul coup on n'a plus du tout cette arrogance de l'anthropocène.
[01:52.800 --> 01:58.680]  On se dit oui là ça se rapproche, c'est plutôt une chute qui s'approche. Ça peut être utile pour
[01:58.680 --> 02:04.980]  inverser les récits, pour inverser notre place dans l'anthropocène, de jouer avec avec tous ces
[02:04.980 --> 02:11.100]  récits pour percevoir un monde en accélération n'est pas nécessairement quelque chose de positif.
[02:11.100 --> 02:17.100]  L'accélération ça peut être d'accélérer en klaxonnant dans le mur. Donc c'est un petit peu
"""

EXPECTED_OUT = """[00]
Bienvenue dans ce vingtième et dernier épisode du Grand course à tort sur la robustesse. On va parler de la transformation. La question qu'on se pose c'est comment transformer, comment basculer de la performance à la robustesse. Pour transformer, il faut 3 ingrédients. Le premier c'est de l'éducation, il faut s'éduquer. Le deuxième il faut s'arrêter, il faut créer de l'espace pour pouvoir se transformer. Et le troisième ingrédient c'est un récit, il faut un récit pour mobiliser. C'est ça qu'on va explorer dans cet épisode. Je vais commencer avec les récits et avec ces diagrammes de la grande accélération où on voit l'impact des humains dans l'anthropocène où

[01]
tout s'accélère depuis les années 50. Quand on voit ces courbes, elles peuvent nous faire un peu froid dans le dos mais on a derrière dans un coin de notre tête l'idée un petit peu de l'arrogance de l'humain de l'anthropocène qui se dit on a été capable de faire ça, d'avoir une dynamique exponentielle, de créer tous ces biens de consommation, toutes ces organisations à cet impact énorme et finalement il y a une forme d'attraction. C'est un peu comme le papillon qui regarde la flamme. Alors moi ce que je vous propose pour inverser ce récit là, c'est tout simplement d'inverser la courbe. Vraiment de l'inverser géométriquement et observer l'effet psychologique que ça a sur vous. De voir ces courbes qui maintenant tombent rapidement, d'un seul coup on n'a plus du tout cette arrogance de l'anthropocène. On se dit oui là ça se rapproche, c'est plutôt une chute qui s'approche. Ça peut être utile pour inverser les récits, pour inverser notre place dans l'anthropocène, de jouer avec avec tous ces

[02]
récits pour percevoir un monde en accélération n'est pas nécessairement quelque chose de positif. L'accélération ça peut être d'accélérer en klaxonnant dans le mur. Donc c'est un petit peu"""



def test_transform_sample():
    out = transform_subtitles(SAMPLE_IN)
    assert out == EXPECTED_OUT