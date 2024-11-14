from glob import glob
import os 


def delete_recommendation_log_files():
    """
    Supprime les fichiers de log de recommandation de l'IA.
    Les fichiers de log sont des fichiers texte nomm s "computers_info_<timestamp>.txt"
    qui contiennent les informations sur les ordinateurs que l'IA a recommand s.
    Cette fonction supprime tous les fichiers de log present dans le dossier.
    """
    # Chemin vers le dossier contenant les fichiers de log
    path = os.path.dirname(os.path.realpath(__file__))
    path_files = os.path.join(path, "computers_info_*.txt")

    # Liste des fichiers logs de l'ia
    files = glob(path_files)

    # Suppression des fichiers
    for file in files:
        os.remove(file)
        
    # Oblige la fonction à s'arreter
    return