import tkinter as tk
from tkinter import ttk

from grascii.defaults import SEARCH
from grascii.dictionary.list import get_built_ins, get_installed
from grascii.regen import SearchMode
from grascii.searchers import GrasciiSearcher

DEFAULT_PADDING = 8


class Application(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack(fill=tk.BOTH, expand=True)
        self.results_content = tk.StringVar()
        self.search_mode = tk.StringVar(value=SEARCH["SearchMode"])
        self.interpretation = tk.StringVar(value=SEARCH["Interpretation"])
        self.uncertainty = tk.IntVar(value=SEARCH.getint("Uncertainty"))
        self.fix_first = tk.BooleanVar(value="false")
        self.annotation_mode = tk.StringVar(value=SEARCH["AnnotationMode"])
        self.aspirate_mode = tk.StringVar(value=SEARCH["AspirateMode"])
        self.disjoiner_mode = tk.StringVar(value=SEARCH["DisjoinerMode"])

        self.default_dictionaries = SEARCH["Dictionary"].split()
        self.available_dicts = set(self.default_dictionaries)
        installed = map(lambda s: ":" + s, get_installed())
        built_ins = map(lambda s: ":" + s, get_built_ins())
        self.available_dicts.update(installed, built_ins)
        self.dictionaries = tk.StringVar(value=list(self.available_dicts))
        self.create_widgets()

    def create_widgets(self):
        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)
        self.create_search_bar()
        self.create_settings_frame()
        self.create_results_frame()

    def create_search_bar(self):
        def search():
            dictionary_indices = self.lst_dictionaries.curselection()
            dictionaries = [
                d
                for i, d in enumerate(list(self.available_dicts))
                if i in dictionary_indices
            ]
            searcher = GrasciiSearcher(dictionaries=dictionaries)
            grascii = ent_search.get()
            results = searcher.search(
                grascii=grascii,
                search_mode=self.search_mode.get(),
                interpretation=self.interpretation.get(),
                uncertainty=self.uncertainty.get(),
                fix_first=self.fix_first.get(),
                annotation_mode=self.annotation_mode.get(),
                aspirate_mode=self.aspirate_mode.get(),
                disjoiner_mode=self.disjoiner_mode.get(),
            )
            if results is not None:
                if len(results) > 2000:
                    self.results_content.set(
                        f"Results: {len(results)} (Only displaying the first 2000)\n\n"
                        + "\n".join(results[:2000])
                    )
                else:
                    self.results_content.set(
                        f"Results: {len(results)}\n\n" + "\n".join(results)
                    )

        def search_event(event):
            search()

        frm_search = tk.Frame(master=self)
        frm_search.grid(
            row=0, column=1, sticky="nw", padx=DEFAULT_PADDING, pady=DEFAULT_PADDING
        )
        ent_search = tk.Entry(master=frm_search)
        ent_search.bind("<Return>", search_event)
        ent_search.pack(fill=tk.Y, side=tk.LEFT, padx=DEFAULT_PADDING)
        btn_search = tk.Button(master=frm_search, text="Search", command=search)
        btn_search.pack(fill=tk.Y, side=tk.LEFT)

    def create_settings_frame(self):
        frm_settings = tk.Frame(master=self, relief=tk.GROOVE, borderwidth=5)
        frm_settings.grid(
            row=1, column=0, padx=DEFAULT_PADDING, pady=DEFAULT_PADDING, sticky="n"
        )
        lbl_settings = tk.Label(master=frm_settings, text="Settings")
        lbl_settings.grid(row=0, column=0, columnspan=2, pady=DEFAULT_PADDING)
        lbl_search_mode = tk.Label(master=frm_settings, text="Search Mode")
        lbl_search_mode.grid(row=1, column=0, padx=DEFAULT_PADDING)
        spn_search_mode = ttk.Spinbox(
            master=frm_settings,
            textvariable=self.search_mode,
            values=[member.value for member in SearchMode],
        )
        spn_search_mode.grid(
            row=1, column=1, pady=DEFAULT_PADDING / 2, padx=DEFAULT_PADDING
        )
        spn_search_mode.state(["readonly"])
        lbl_interpretation = tk.Label(master=frm_settings, text="Interpretation")
        lbl_interpretation.grid(row=2, column=0, padx=DEFAULT_PADDING)
        spn_interpretation = ttk.Spinbox(
            master=frm_settings,
            textvariable=self.interpretation,
            values=["best", "all"],
        )
        spn_interpretation.grid(
            row=2, column=1, pady=DEFAULT_PADDING / 2, padx=DEFAULT_PADDING
        )
        spn_interpretation.state(["readonly"])
        lbl_uncertainty = tk.Label(master=frm_settings, text="Uncertainty")
        lbl_uncertainty.grid(row=3, column=0, padx=DEFAULT_PADDING)
        spn_uncertainty = ttk.Spinbox(
            master=frm_settings, from_=0, to=2, textvariable=self.uncertainty
        )
        spn_uncertainty.grid(
            row=3, column=1, pady=DEFAULT_PADDING / 2, padx=DEFAULT_PADDING
        )
        spn_uncertainty.state(["readonly"])
        lbl_fix_first = tk.Label(master=frm_settings, text="Fix First")
        lbl_fix_first.grid(row=4, column=0, padx=DEFAULT_PADDING)
        chk_fix_first = tk.Checkbutton(master=frm_settings, variable=self.fix_first)
        chk_fix_first.grid(
            row=4, column=1, pady=DEFAULT_PADDING / 2, padx=DEFAULT_PADDING
        )
        lbl_annotation_mode = tk.Label(master=frm_settings, text="Annotation Mode")
        lbl_annotation_mode.grid(row=5, column=0, padx=DEFAULT_PADDING)
        spn_annotation_mode = ttk.Spinbox(
            master=frm_settings,
            textvariable=self.annotation_mode,
            values=["discard", "retain", "strict"],
        )
        spn_annotation_mode.grid(
            row=5, column=1, pady=DEFAULT_PADDING / 2, padx=DEFAULT_PADDING
        )
        spn_annotation_mode.state(["readonly"])
        lbl_aspirate_mode = tk.Label(master=frm_settings, text="Aspirate Mode")
        lbl_aspirate_mode.grid(row=6, column=0, padx=DEFAULT_PADDING)
        spn_aspirate_mode = ttk.Spinbox(
            master=frm_settings,
            textvariable=self.aspirate_mode,
            values=["discard", "retain", "strict"],
        )
        spn_aspirate_mode.grid(
            row=6, column=1, pady=DEFAULT_PADDING / 2, padx=DEFAULT_PADDING
        )
        spn_aspirate_mode.state(["readonly"])
        lbl_disjoiner_mode = tk.Label(master=frm_settings, text="Disjoiner Mode")
        lbl_disjoiner_mode.grid(row=7, column=0, padx=DEFAULT_PADDING)
        spn_disjoiner_mode = ttk.Spinbox(
            master=frm_settings,
            textvariable=self.disjoiner_mode,
            values=["discard", "retain", "strict"],
        )
        spn_disjoiner_mode.grid(
            row=7, column=1, pady=DEFAULT_PADDING / 2, padx=DEFAULT_PADDING
        )
        spn_disjoiner_mode.state(["readonly"])
        lbl_dictionaries = tk.Label(master=frm_settings, text="Dictionaries")
        lbl_dictionaries.grid(row=8, column=0, sticky="n", pady=DEFAULT_PADDING)
        self.lst_dictionaries = tk.Listbox(
            master=frm_settings,
            listvariable=self.dictionaries,
            selectmode="extended",
            exportselection=False,
        )
        for i, dictionary in enumerate(list(self.available_dicts)):
            if dictionary in self.default_dictionaries:
                self.lst_dictionaries.selection_set(i)
        self.lst_dictionaries.grid(
            row=8, column=1, sticky="ew", pady=DEFAULT_PADDING, padx=DEFAULT_PADDING
        )

    def create_results_frame(self):
        canvas = tk.Canvas(master=self, width=300, relief=tk.GROOVE, borderwidth=5)
        lbl_results = tk.Label(
            master=canvas, textvariable=self.results_content, justify=tk.LEFT
        )
        canvas.create_window(
            (DEFAULT_PADDING * 2, DEFAULT_PADDING * 2), anchor="nw", window=lbl_results
        )
        scroll_results = ttk.Scrollbar(
            master=self, orient=tk.VERTICAL, command=canvas.yview
        )
        canvas.configure(yscrollcommand=scroll_results.set)
        scroll_results.grid(
            row=1, column=2, sticky="ns", padx=DEFAULT_PADDING, pady=DEFAULT_PADDING
        )
        canvas.grid(
            row=1, column=1, sticky="nesw", padx=DEFAULT_PADDING, pady=DEFAULT_PADDING
        )
        lbl_results.bind(
            "<Configure>",
            lambda event, canvas=canvas: canvas.configure(
                scrollregion=canvas.bbox("all")
            ),
        )
