import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handleCreaGrafo(self,e):
        self._model.buildGraph()
        self._view.lst_result.controls.clear()
        self._view.lst_result.controls.append(ft.Text("Grafo correttamente creato"))
        self._view.lst_result.controls.append(ft.Text(f"Il grafo contiene {self._model.getNumNodi()} nodi"))
        self._view.lst_result.controls.append(ft.Text(f"Il grafo contiene {self._model.getNumArchi()} archi"))
        self._view._btnCalcola.disabled = False #una volta creato il grafo, ABILITO il bottone per poter cercare i cammini possibili
        self._view.update_page()

    def handleCercaRaggiungibili(self,e):
        if self._fermataPartenza is None: #la partenza deve essere la Fermata selezionata dall'utente
            self._view.lst_result.controls.clear()
            self._view.lst_result.controls.append(ft.Text("Attenzione, stazione di partenza non selezionata", color='red'))
            self._view.update_page()
            return

        nodes=self._model.getBFSNodesFromEdges(self._fermataPartenza)
        self._view.lst_result.controls.clear()
        self._view.lst_result.controls.append(ft.Text(f"Di seguito le stazioni raggiungibili a partire da {self._fermataPartenza}"))
        for n in nodes:
            self._view.lst_result.controls.append(ft.Text(f"{n}"))
        self._view.update_page()




    def loadFermate(self, dd: ft.Dropdown()):
        fermate = self._model.fermate

        if dd.label == "Stazione di Partenza":
            for f in fermate:
                dd.options.append(ft.dropdown.Option(text=f.nome,
                                                     data=f,
                                                     on_click=self.read_DD_Partenza))
        elif dd.label == "Stazione di Arrivo":
            for f in fermate:
                dd.options.append(ft.dropdown.Option(text=f.nome,
                                                     data=f,
                                                     on_click=self.read_DD_Arrivo))

    def read_DD_Partenza(self,e):
        print("read_DD_Partenza called ")
        if e.control.data is None:
            self._fermataPartenza = None
        else:
            self._fermataPartenza = e.control.data

    def read_DD_Arrivo(self,e):
        print("read_DD_Arrivo called ")
        if e.control.data is None:
            self._fermataArrivo = None
        else:
            self._fermataArrivo = e.control.data
