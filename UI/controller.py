import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handleCerca(self,e):
        source = self._model.getNodeFromId(int(self._view._txtIdOggetto.value))
        lun = self._view._ddLun.value

        if lun is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Attenzione ! Selezionare un valore di lunghezza tra le scelte", color="red"))
            self._view.update_page()
            return

        lunInt = int(lun)

        path,cost = self._model.getOptPath(source,lunInt)
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(
            ft.Text(f"Ho trovato un cammino che parte da {source} e costa {cost} "))
        self._view.txt_result.controls.append(
            ft.Text(f"Di seguito i nodi che compongono il cammino:"))

        for p in path:
            self._view.txt_result.controls.append(
                ft.Text(p))

        self._view.update_page()


    def handleAnalizzaOggetti(self, e):
        self._model.buildGraph()
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text("Grafo correttamente creato."))
        self._view.txt_result.controls.append(
            ft.Text(f"Il grafo contiene {self._model.getNumNodes()} nodi e {self._model.getNumEdges()} archi."))
        self._view._txtIdOggetto.disabled = False
        self._view._btnCompConnessa.disabled = False
        self._view.update_page()

    def handleCompConnessa(self,e):
        idOggetto = None
        txtIdOggetto = self._view._txtIdOggetto.value

        if txtIdOggetto == "":
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Attenzione, inserire un valore nel campo id", color="red"))
            self._view.update_page()
            return

        try:
            idOggetto = int(txtIdOggetto)
        except ValueError:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Attenzione, inserire un valore numerico nel campo id", color="red"))
            self._view.update_page()
            return

        if not self._model.hasNode(idOggetto):
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text("Attenzione, id non presente", color="red"))
            self._view.update_page()
            return

        sizeCompConn = self._model.getInfoCompConnessa(idOggetto)
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(
            ft.Text(f"La componente connessa contenente l'oggetto con id {idOggetto} è composta di {sizeCompConn} nodi", color="green"))
        self._view.update_page()

        # Sblocco dei componenti (assicurati che i nomi corrispondano a View)
        self._view._ddLun.disabled = False
        self._view._btnCerca.disabled = False

        # Creazione della lista di opzioni
        lunValues = list(range(2, sizeCompConn))

        # PULIZIA: Rimuovi le opzioni precedenti
        self._view._ddLun.options.clear()

        # POPOLAMENTO: Usa un ciclo for o list comprehension (non solo map)
        for lun in lunValues:
            self._view._ddLun.options.append(ft.dropdown.Option(str(lun)))

        # REFRESH: Fondamentale per vedere i cambiamenti nel Dropdown
        self._view.update_page()
