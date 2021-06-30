# -*- coding: utf-8 -*-
"""
Created on Wed Apr 14 15:37:22 2021

@author: Dgrey
"""


from sys import exc_info, maxsize
import tkinter as tk
from tkinter import Toplevel, ttk
from tkinter import messagebox
from tkinter import filedialog
from tkinter.colorchooser import askcolor
import os
import random
import re

import logging
from logging.handlers import RotatingFileHandler
from typing import Sized





formatter = logging.Formatter("%(asctime)s ## %(levelname)s ## %(funcName)s -- Ligne %(lineno)s \n\t %(message)s \n\n")

handler_critic = logging.FileHandler("log_critic.log", mode = "a", encoding = "utf-8")
handler_erreur = logging.FileHandler("log_error.log", mode = "a", encoding = "utf-8" )
handler_warning = logging.FileHandler("log_warning.log", mode = "a", encoding = "utf-8")
handler_info = logging.FileHandler("log_info.log", mode = "a", encoding = "utf-8")
handler_debug = logging.FileHandler("log_debug.log", mode = "a", encoding = "utf-8")

handler_critic.setFormatter(formatter)
handler_erreur.setFormatter(formatter)
handler_warning.setFormatter(formatter)
handler_info.setFormatter(formatter)
handler_debug.setFormatter(formatter)

handler_critic.setLevel(logging.CRITICAL)
handler_erreur.setLevel(logging.ERROR)
handler_warning.setLevel(logging.WARNING)
handler_info.setLevel(logging.INFO)
handler_debug.setLevel(logging.DEBUG)

logger = logging.getLogger("Dico_langue")
logger.setLevel(logging.DEBUG) # criticité minium voulu
logger.addHandler(handler_critic)
logger.addHandler(handler_erreur)
logger.addHandler(handler_warning)
logger.addHandler(handler_info)
logger.addHandler(handler_debug)




class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Dictionnaire de langue")
        

        self.update_idletasks()
        self.width_display = self.winfo_screenwidth()
        self.height_display = self.winfo_screenheight()
        x, y = int(self.width_display / 3), int(self.height_display / 3)

        self.master.geometry(f"600x400+{x}+{y}")
        self.master.resizable(False, False)
       
        self.path_dossier = os.getcwd()
        
        try :
            self.nom_icon = os.path.join(self.path_dossier, "Icon.ico")
            self.master.iconbitmap(False, self.nom_icon)
        except Exception as e :
            logger.warning(msg = f"Icon non trouvé : {str(e)}")

        self.pack()

        self.menu = tk.Menu(self.master)
        self.master.config(menu = self.menu)

        self.file_menu = tk.Menu(self.menu, tearoff = 0)

        try :
            self.file_menu.add_command(label = "A propos", command = About)
        except Exception as e :
            logger.critical(f"About crash : {str(e)}")

        self.menu.add_cascade(label = "Option", menu = self.file_menu)

        self.dico_type_langue = {}
        self.dico_listbox_langue = {}
        self.dico = {}
        self.dico_mot = {}
        self.language = []
        
        self.var_cbb_treeview = tk.StringVar()
        self.var_cbb_langue = tk.StringVar()
        self.var_entry_toplevel_abre_lang = tk.StringVar()
        self.var_entry_toplevel_nom_lang = tk.StringVar()   
        self.var_traduction = tk.StringVar()
        self.var_langage_trad = tk.StringVar()
        self.var_entry_mot = tk.StringVar()
        self.var_entry_search = tk.StringVar()
        
        self.var_comment = tk.StringVar()
        self.var_comment.set("Libelle")
        self.var_edit = False
        
        self.var_bt_toplevel_bt_valider = tk.StringVar()
        
        Manage_File(self).construct("load_all", self.init_data_for_class())

        self.create_frame()
        self.create_widgets()


    def init_data_for_class(self) :
        data = {}
        data["path_dossier"] = self.path_dossier
        data["dico_listbox_langue"] = self.dico_listbox_langue
        data["language"] = self.language
        data["dico_mot"] = self.dico_mot
        data["dico"] = self.dico
        data["var_comment"] = self.var_comment
        data["var_entry_mot"] = self.var_entry_mot.get()
        data["var_cbb_langue"] = self.var_cbb_langue.get()
        data["var_traduction"] = self.var_traduction.get()
        data["var_langage_trad"] = self.var_langage_trad.get()
        data["var_edit"] = self.var_edit
        
        return data


    def create_frame(self) :
        self.update_idletasks()        
        self.frame_entry_user = tk.Frame(self)
        self.frame_entry_user.pack(side = "left", expand = True, fill = tk.BOTH, padx = 10, pady = 5)
        
        self.frame_entry_user_top = tk.Frame(self.frame_entry_user)
        self.frame_entry_user_top.pack(side= "top", expand = True, fill = tk.X, anchor = "nw")
        
        self.frame_entry_user_mid = tk.Frame(self.frame_entry_user)
        self.frame_entry_user_mid.pack(side= "top", expand = True, fill = tk.X, anchor = "nw")
        
        self.frame_entry_user_bottom = tk.Frame(self.frame_entry_user)
        self.frame_entry_user_bottom.pack(side= "top", expand = True, fill = tk.X)
        
        
        self.sp_master = ttk.Separator(self, orient = "vertical")
        self.sp_master.pack(side = "left", expand = True, fill = tk.BOTH, anchor = "center")



        self.frame_dico = tk.Frame(self)
        self.frame_dico.pack(side = "left", anchor = "e", expand = True, fill = tk.BOTH, padx = 5, pady = 5)

        self.frame_dico_head = tk.Frame(self.frame_dico)
        self.frame_dico_head.pack()
        
        root.update_idletasks()
        self.frame_dico_treeview = tk.Frame(self.frame_dico, width = self.winfo_width() * 0.7)
        self.frame_dico_treeview.pack(side = "left", padx = 5)
                
        self.frame_dico_treeview_right = tk.Frame(self.frame_dico_treeview)
        self.frame_dico_treeview_right.pack(side = "right", expand = True, fill = tk.BOTH, padx = 15)

        self.frame_dico_treeview_bottom = tk.Frame(self.frame_dico_treeview)
        self.frame_dico_treeview_bottom.pack(side = "bottom", expand = True, fill = tk.X)


        self.canvas_treeview = tk.Canvas(self.frame_dico_treeview, width = self.winfo_width() * 0.7, height = 20)
        self.canvas_treeview.pack(side = "left")        



        self.frame_test = tk.Frame(self.frame_entry_user)
        self.frame_test.pack(side = "bottom", expand = True, fill = tk.X)


    def widgets_user(self) :
        try :
            if self.cbb_langue_user.winfo_exists() == 1 :
                self.cbb_langue_user.destroy()
        except :
            pass
        
        self.lb_mot = tk.Label(self.frame_entry_user_top, text = "Nouveau mot : ")
        self.lb_mot.grid(column=0, row=0, sticky = "w")
        
        self.entry_mot = tk.Entry(self.frame_entry_user_top, textvariable = self.var_entry_mot, width = 30)
        self.entry_mot.grid(column=1, row=0, sticky = "w")    
        
        self.lb_langue = tk.Label(self.frame_entry_user_top, text = "Langue : ")
        self.lb_langue.grid(column=0, row=1, sticky = "w")

        self.cbb_langue_user = ttk.Combobox(self.frame_entry_user_top, textvariable = self.var_cbb_langue, values = self.language, state = "readonly", width = 12)
        self.cbb_langue_user.grid(row = 1, column = 1, sticky = "w")
        self.var_cbb_langue.set(self.language[0])
        
        self.cbb_langue_user.bind("<<ComboboxSelected>>", self.choix_treeview)
        
        self.bt_valider = tk.Button(self.frame_entry_user_top, text = "Valider", command = self.valider)
        self.bt_valider.grid(column=0, row=4, sticky = "w")
        
        if len(self.dico) != 0 :
            self.sp_test = ttk.Separator(self.frame_test, orient = "horizontal")
            self.sp_test.grid(row = 0, column = 0, sticky = "we", ipadx = 10)

            self.bt_test = tk.Button(self.frame_test, text = "Test tes compétences !", command = self.go_test)
            self.bt_test.grid(row = 1, column = 0, pady = 10)


    def go_test(self) :
        data = {"dico":self.dico, "dico_listbox_langue":self.dico_listbox_langue}
        try :
            Test(self).construct(data)
        except Exception as e :
            logger.critical(f"Test crash : {str(e)}")


    def create_widgets(self):
        # User
        self.widgets_user()
        
        # Treeview
        self.bt_actualiser = tk.Button(self.frame_dico_head, text = "Actualiser : ", command = self.update_treeview)
        self.bt_actualiser.grid(row = 0, column = 0, sticky = "we", columnspan = 5)
        
        self.construct_treeview()
        
        self.lb_search = tk.Label(self.frame_dico_head, text = "Rechercher : ")
        self.lb_search.grid(row = 1, column = 0, sticky = "w", padx = 5, pady = 5)
        
        self.entry_search = tk.Entry(self.frame_dico_head, textvariable = self.var_entry_search)
        self.entry_search.grid(row = 1, column = 1, sticky = "w", pady = 5)
        
        self.bt_search = tk.Button(self.frame_dico_head, text = "search", command = self.search)
        self.bt_search.grid(row = 1, column = 2, sticky = "w", pady = 5)
        

    def choix_treeview(self, event) :
        self.new = False

        if self.var_edit != True :
            try :
                for child in self.treeview.winfo_children() :
                    child.destroy()
                self.construct_treeview()
            except :
                pass
     
        try :
            if self.var_cbb_treeview.get() == "---New---" :
                self.new = True
        except :
            pass
        
        try :
            if self.var_cbb_langue.get() == "---New---" :
                self.new = True
        except :
            pass
        
        try :
            if self.var_langage_trad.get() == "---New---" :
                self.new = True
        except :
            pass
        
        if self.new == True :
            try :
                New_Trad(self).construct(self.init_data_for_class())
            except Exception as e :
                logger.critical(f"New Trad crash : {str(e)}")

            self.frame_entry_user.bind("<FocusOut>", self.update_language_part1)
   
        else : 
            if self.var_edit == False :
                self.construct_treeview()
  

    def construct_treeview(self) :
        try : 
            if self.treeview.winfo_exists() == 1 :
                for child in self.treeview.winfo_children() :
                    child.destroy()
                self.treeview.destroy()
        except :
            pass

        Manage_File(self).construct("load_dictionnaire", self.init_data_for_class())

        data = {}
        data['var_entry_search'] = self.var_entry_search
        data['dico'] = self.dico

        data_tree = Treeview(self).construct(data)

        
        colonne = data_tree[0]
        data_ligne = data_tree[1]
        
        self.treeview = ttk.Treeview(self.canvas_treeview, height = 15)
        self.treeview.pack(expand = True, fill = tk.BOTH)
            
        try :
            if self.verti_scrollbar.winfo_exists() == 1 :
                self.treeview['yscrollcommand'] = self.verti_scrollbar.set
                self.verti_scrollbar['command'] = self.treeview.yview
    
            if self.horti_scrollbar.winfo_exists() == 1 :
                self.treeview['xscrollcommand'] = self.horti_scrollbar.set
                self.horti_scrollbar['command'] = self.treeview.xview

        except :
            try :
                self.verti_scrollbar = ttk.Scrollbar(self.frame_dico_treeview_right, orient = "vertical")
                self.verti_scrollbar['command'] = self.treeview.yview
                self.verti_scrollbar.pack(side = "right", expand = True, fill=tk.Y, padx = 15)
                self.treeview['yscrollcommand'] = self.verti_scrollbar.set
                
                self.horti_scrollbar = ttk.Scrollbar(self.frame_dico_treeview_bottom, orient = "horizontal")
                self.horti_scrollbar['command'] = self.treeview.xview
                self.horti_scrollbar.pack(expand = True, fill=tk.X, pady = 10)
                self.treeview['xscrollcommand'] = self.horti_scrollbar.set
                    
                self.treeview.config(scrollregion = self.canvas_treeview.bbox('all'))
                
            except :
                pass

        self.treeview["columns"] = colonne
        self.treeview["show"] = "headings"

        for k in range(0, len(colonne)) :
            if len(colonne) == 1 :
                self.treeview.column(k, width = 250)
            if len(colonne) == 2 :
                self.treeview.column(k, width = 125)
        
            self.treeview.column(k, anchor = "w", minwidth = 50, width = 80)
            self.treeview.heading(k, text = colonne[k])
        
        count_ligne = 0
        for key, var in enumerate(self.dico.items()) :
            self.treeview.insert("", "end", key, values = data_ligne[count_ligne])
            count_ligne += 1

        self.treeview.bind("<Double-Button-1>", self.bind_treeview_double_click)

        
    def bind_treeview_double_click(self, event) :
        item = self.treeview.selection()[0]
        nom = self.treeview.item(item)["values"][0]

        data = {}
        data['dico'] = self.dico
        data['var_comment'] = self.var_comment
        data['var_langage_trad'] = self.var_langage_trad
        data['var_cbb_treeview'] = self.var_cbb_treeview
        data['var_cbb_langue'] = self.var_cbb_langue
        data['language'] = self.language
        data['path_dossier'] = self.path_dossier
        data['dico_listbox_langue'] = self.dico_listbox_langue
        data['item'] = item
        data['nom'] = nom
        data["dico_mot"] = self.dico_mot
        data["var_entry_mot"] = self.var_entry_mot.get()
        data["var_traduction"] = self.var_traduction.get()
        data["var_edit"] = self.var_edit

        try :
            Edit(self).construct(data)
        except Exception as e :
            logger.critical(f"Edit crash : {str(e)}")

        self.update_treeview()
        self.bind("<FocusOut>", self.update_language_part1)
    

    def search(self) :
        self.var_search_mot = self.var_entry_search.get()
    
        if self.var_search_mot != "" :
            self.var_entry_search.set("")
            
            for key, var in enumerate(self.dico.items()) :
                for value in self.treeview.item(key)["values"] :
                    if value == self.var_search_mot :
                        self.treeview.focus(key)
                        self.treeview.see(key)
                        self.treeview.selection_set(key)
                        break
                else :
                    continue
                break
 
             
    def valider(self) :        
        if self.var_entry_mot.get() == "" :
            tk.messagebox.showerror("Erreur", "Erreur formulaire !")
            
        else :
            if self.verif_exist_mot() != True :
                self.bt_valider.destroy()
                try :
                    try :
                        for child in self.frame_entry_user_mid.winfo_children() :
                            child.destroy()
                        for child in self.frame_entry_user_bottom.winfo_children() :
                            child.destroy()
                    except :
                        pass

                    try :
                        if self.sp_ajout.winfo_exists() == 1 :
                            self.sp_ajout.destroy()
                    except :
                        pass

                    try :
                        if self.sp_enregistrer.winfo_exists() == 1 :
                            self.sp_enregistrer.destroy()
                    except :
                        pass

                    self.sp_ajout = ttk.Separator(self.frame_entry_user_mid, orient = "horizontal")
                    self.sp_ajout.grid(row = 4, column = 0, columnspan = 5, pady = 10, sticky = "we")
                    
                    self.lb_trad_mot = tk.Label(self.frame_entry_user_mid, text = "Traduction : ")
                    self.lb_trad_mot.grid(row = 5, column = 0, sticky = "w")
                    
                    self.var_traduction.set("")
                    self.entry_trad = tk.Entry(self.frame_entry_user_mid, textvariable = self.var_traduction, width = 32)
                    self.entry_trad.grid(row = 5, column = 1, sticky = "w")
                    
                    self.lb_trad_langue = tk.Label(self.frame_entry_user_mid, text = "Langue : ")
                    self.lb_trad_langue.grid(row = 6, column = 0, sticky = "w")
                    
                    for k in self.language :
                        if k != self.var_cbb_langue.get() and k != "---New---" :
                            self.var_langage_trad.set(k)
                    
                    try :
                        if self.cbb_langage_trad.winfo_exists() == 1 :
                            self.cbb_langage_trad.update()
                    except :
                        pass

                    self.cbb_langage_trad = ttk.Combobox(self.frame_entry_user_mid, textvariable = self.var_langage_trad, values = self.language, state = "readonly", width = 12)
                    self.cbb_langage_trad.grid(row = 6, column = 1, sticky = "w")
                    
                    self.cbb_langage_trad.bind("<<ComboboxSelected>>", self.choix_treeview)
                    
                    self.lb_comment = tk.Label(self.frame_entry_user_mid, text = "Explication : ")
                    self.lb_comment.grid(row = 7, column = 0, sticky = "w")
                    
                    self.txt_comment = tk.Text(self.frame_entry_user_mid, width = 24, height = 2, wrap = None)
                    self.txt_comment.grid(row = 7, column = 1, sticky = "w")
                
                    self.sp_enregistrer = ttk.Separator(self.frame_entry_user_mid, orient = "horizontal")
                    self.sp_enregistrer.grid(row = 8, column = 0, columnspan = 5, pady = 10, sticky = "we")
                    
                    self.bt_enregistrer = tk.Button(self.frame_entry_user_bottom, text = "Enregistrer", command = self.enregistrer)
                    self.bt_enregistrer.grid(row = 9, column = 0, sticky = "w", padx = 10)
                    
                    self.bt_toplevel_annuler = tk.Button(self.frame_entry_user_bottom, text = "Annuler", command = self.annuler)
                    self.bt_toplevel_annuler.grid(row = 9, column = 1, columnspan = 4, sticky = "e", padx = 10)
                
                except Exception as e :
                    logger.warning(msg = f"Echec recréation après valider new mot : {str(e)}")

            else :
                tk.messagebox.showerror("Erreur", "Mot déja existant")
              
    
    def annuler(self) :
        for child in self.frame_entry_user.winfo_children() :
            child.destroy()
    
        self.var_entry_mot.set("")

        self.frame_entry_user_top = tk.Frame(self.frame_entry_user)
        self.frame_entry_user_top.pack(side= "top", expand = True, fill = tk.X, anchor = "nw")
        
        self.frame_entry_user_mid = tk.Frame(self.frame_entry_user)
        self.frame_entry_user_mid.pack(side= "top", expand = True, fill = tk.X, anchor = "nw")
        
        self.frame_entry_user_bottom = tk.Frame(self.frame_entry_user)
        self.frame_entry_user_bottom.pack(side= "top", expand = True, fill = tk.X, anchor = "nw")
        
        self.frame_test = tk.Frame(self.frame_entry_user)
        self.frame_test.pack(side = "bottom", expand = True, fill = tk.X)
        
        self.widgets_user()
   

    def enregistrer(self) :
        if self.var_traduction.get() != "" and self.var_langage_trad.get() != "" :
            self.var_comment = self.txt_comment.get("1.0", "end-1c")
            if self.var_comment == "" or self.var_comment == None :
                self.var_comment = "libelle"

            data = {}
            data['var_entry_mot'] = self.var_entry_mot.get()
            data['var_cbb_langue'] = self.var_cbb_langue.get()
            data['var_traduction'] = self.var_traduction.get()
            data['var_langage_trad'] = self.var_langage_trad.get()
            data['var_comment'] = self.var_comment
            data['dico_listbox_langue'] = self.dico_listbox_langue
            data['path_dossier'] = self.path_dossier

            Manage_File(self).construct("save_entry", data)
            
            try :
                self.sp_enregistrer.destroy()
                self.sp_ajout.destroy()
                self.sp_test.destroy()
            except :
                pass


            try :
                for child in self.frame_entry_user_top.winfo_children() :
                    child.destroy()
                    
                for child in self.frame_entry_user_mid.winfo_children() :
                    child.destroy()
                    
                for child in self.frame_entry_user_bottom.winfo_children() :
                    child.destroy()
           
            except :
                pass

            self.var_entry_mot.set("")
            
            try :
                self.widgets_user()
            except Exception as e :
                logger.warning(msg = f"Reconstruction widget user après enregistrer : {str(e)}")

            try :
                self.treeview.destroy()
            except :
                pass

            try :
                self.construct_treeview()
            except Exception as e :
                logger.warning(msg = f"Recontruction treeview/construct_treeview : {str(e)}")

            tk.messagebox.showinfo("Enregistré", "Nouvelle entrée ajouté !")
    
        else :
            tk.messagebox.showerror("Erreur", "Erreur formulaire !")

       
    def verif_exist_mot(self) :
        for iid, dic in self.dico.items() :
            for name, value in dic.items() :                
                if name == "mot" :
                    for k in value :
                        try :
                            if k == self.var_entry_mot.get() :
                                return True     # il existe
                        except Exception as e :
                            logger.error(msg = f"Echec verif mot {str(e)}")
                        
     
    def update_treeview(self) :
        try :
            for child in self.treeview.winfo_children() :
                child.destroy()
            self.treeview.destroy()
        except :
            pass

        self.construct_treeview()


    def update_language_part1(self, event) :
        if self.var_cbb_langue.get() == "---New---" and self.new == True :
            self.frame_entry_user.bind("<FocusIn>", self.update_language)


    def update_language(self, event) :
        self.language = []
        try :            
            f = open(os.path.join(self.path_dossier, "Langue.txt"), "r")
            txt = f.read()
            f.close()
            
            try :
                txt = txt.split("\n")
                for k in txt :
                    if k != "" :
                        k = k.split(":")
                        self.dico_listbox_langue[k[0]] = k[1]
            except Exception as e :
                logger.error(msg = f"Erreur index langue : {str(e)}")
            
        except Exception as e :
            logger.info(msg = f"Fichier langue inexistant pendant update : {str(e)}")
            f = open("Langue.txt", "w")
            f.close()

        for abre, nom in self.dico_listbox_langue.items():
            self.language.append(nom)

        self.language.append("---New---")        
        self.new = False
        
        try :
            if self.cbb_langue_user.winfo_exists() == 1 :
                self.cbb_langue_user.update()
                self.cbb_langue_user.config(textvariable = self.var_cbb_langue, values = self.language)
        except :
            pass

        try :
            if self.cbb_langage_trad.winfo_exists() == 1 :
                self.cbb_langage_trad.update()
                self.cbb_langage_trad.config(textvariable = self.var_langage_trad, values = self.language)
        except :
            pass



class Test(tk.Tk) :
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.master = master

        
    def construct(self, *args) :
        # On récupère les données nécessaires
        self.attribution_variabe(*args)

        # On créer la nouvelle fenêtre Test
        self.toplevel_test = tk.Toplevel(self)

        x, y = int(self.winfo_screenwidth() / 3), int(self.winfo_screenheight() / 3)
        self.toplevel_test.geometry(f"350x100+{x+50}+{y+80}")
        self.toplevel_test.resizable(False, False)

        self.toplevel_test.wm_title("Test tes compétences !")

        self.toplevel_test.focus_force()
        self.toplevel_test.grab_set()

        self.frame_toplevel_test_body = tk.Frame(self.toplevel_test)
        self.frame_toplevel_test_body.pack()

        self.toplevel_test_var_reload = False

        self.string()


    def attribution_variabe(self, *args) :
        self.dico = {}
        self.dico_listbox_langue = {}

        try :
            for name, value in args[0].items() :
                if name == "dico_listbox_langue" :
                    self.dico_listbox_langue = value
                if name == "dico" :
                    self.dico = value
                    
        except Exception as e :
            logger.error(msg = f"Echec attribution var : {str(e)}")


    def string(self) :
        # Recherche d'un mot et d'une langue
        self.valide_data = self.aleatoire()

        # On créer le texte à afficher
        mot = self.valide_data["mot"]
        langue = self.valide_data["langue"]
        
        for abre, complet in self.dico_listbox_langue.items() :
            if abre == langue :
                langue = complet

        self.string_test = f"Trouve la traduction de '{mot}' en '{langue}' !"

        if self.toplevel_test_var_reload == False :
            self.widgets()

        if self.toplevel_test_var_reload == True :
            self.lb_toplevel_test.destroy()
            self.lb_toplevel_test = tk.Label(self.frame_toplevel_test_body, text = self.string_test)
            self.lb_toplevel_test.grid(row = 0, column = 0, pady = 5)
            

    def widgets(self) :
        # On construit les widgets
        self.lb_toplevel_test = tk.Label(self.frame_toplevel_test_body, text = self.string_test)
        self.lb_toplevel_test.grid(row = 0, column = 0, pady = 5)

        self.var_entry_toplevel_test = tk.StringVar()
        self.entry_toplevel_test = tk.Entry(self.frame_toplevel_test_body, textvariable = self.var_entry_toplevel_test)
        self.entry_toplevel_test.grid(row = 1, column = 0, sticky = "we", pady = 5, padx = 5)

        self.bt_toplevel_test = tk.Button(self.frame_toplevel_test_body, text = "Valider", command = self.valider)
        self.bt_toplevel_test.grid(row = 1, column = 1, padx = 5, pady = 5)

        self.lb_toplevel_test_info = tk.Label(self.frame_toplevel_test_body, text = "F5 to reload test", foreground = "gray60", font = ("arial", 10, "italic"))
        self.lb_toplevel_test_info.grid(row = 2, column = 0, columnspan = 3)

        self.entry_toplevel_test.bind("<Return>", self.event)
        self.toplevel_test.bind("<F5>", self.reload)
    

    def reload(self, event) :
        self.toplevel_test_var_reload = True
        self.string()
        
    
    def event(self, event) :
        self.valider()


    def valider(self) :
        mot = self.valide_data["mot"]
        langue = self.valide_data["langue"]
        autre_langue = self.valide_data["autre_langue"]
        autre_mot = self.valide_data["autre_mot"]
        langue_asso = self.valide_data["langue_asso"]
        
        mot_entry = self.var_entry_toplevel_test.get()

        resultat_test = False

        for k in range(0, len(autre_mot)) :
            if autre_mot[k] == mot_entry :
                if autre_langue[k] == langue :
                    tk.messagebox.showinfo("Résultat", "Bravo, tu as réussi le test !")
                    resultat_test = True

                    try :
                        for child in self.frame_toplevel_test_body.winfo_children() :
                            child.destroy()
                    except :
                        pass

                    try :
                        self.string()
                        self.widgets()
                    except Exception as e :
                        logger.warning(msg = f"Recréation widget : {str(e)}")

                    break
        
        if resultat_test == False :
            tk.messagebox.showinfo("Résultat", "Perdu, tu feras mieux au prochain coup !")


    def aleatoire(self) :
        valide_data = {}

        alea_entree = random.randint(0, len(self.dico) -1)

        result = self.generateur_alea(alea_entree)
        alea_mot = result[0]
        alea_langue = result[1]

        autre_langue = []
        autre_mot = []
        mot = ""
        langue = ""
        langue_asso = ""
        

        for key, var in enumerate(self.dico.items()) :
            if key == alea_entree :
                for nom, value in self.dico[key].items() :

                    if nom == 'mot' :
                        for k in range(0, len(value)) :
                            if k == alea_mot :
                                mot = value[k]
                            if k != alea_mot :
                                autre_mot.append(value[k])

                    if nom == 'langue' :
                        for k in range(0, len(value)) :
                            if k == alea_langue :
                                langue = value[k]
                                autre_langue.append(value[k])
                            if k != alea_langue :
                                if k == alea_mot :
                                    langue_asso = value[k]
                                else :
                                    autre_langue.append(value[k])


        valide_data = {"mot" : mot, "langue" : langue, "autre_langue" : autre_langue, "autre_mot" : autre_mot, "langue_asso" : langue_asso}

        return valide_data


    def generateur_alea(self, alea_entree) :
        try :
            alea_mot = random.randint(0, len(self.dico[alea_entree]['mot']) -1 )
            alea_langue = random.randint(0, len(self.dico[alea_entree]['langue']) -1 )
            return self.diff(alea_entree, alea_mot, alea_langue)

        except :
            return self.generateur_alea(random.randint(0, len(self.dico)))


    def diff(self, alea_entree, mot, langue) :
        if mot == langue :
            return self.generateur_alea(alea_entree)
        else :
            return mot, langue



class New_Trad(tk.Tk) :
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.master = master


    def construct(self, *args) :
        self.attribution_variable(*args)
        self.tk_toplevel()


    def attribution_variable(self, *args) :
        self.var_entry_toplevel_abre_lang = tk.StringVar()
        self.var_entry_toplevel_nom_lang = tk.StringVar()
        self.var_cbb_toplevel_edit_trad = tk.StringVar()

        for name, value in args[0].items() :
            if name == "var_entry_toplevel_abre_lang" :
                self.var_entry_toplevel_abre_lang = value
            if name == "var_entry_toplevel_nom_lang" :
                self.var_entry_toplevel_nom_lang = value
            if name == "var_cbb_toplevel_edit_trad" :
                self.var_cbb_toplevel_edit_trad = value
            if name == "var_langage_trad" :
                self.var_langage_trad = value
            if name == "var_cbb_treeview" :
                self.var_cbb_treeview = value
            if name == "var_cbb_langue" :
                self.var_cbb_langue = value
            if name == "language" :
                self.language = value
            if name == "path_dossier" :
                self.path_dossier = value
            if name == "dico_listbox_langue" :
                self.dico_listbox_langue = value


    def tk_toplevel(self) :
        self.update_idletasks()
        self.width_display = self.winfo_screenwidth()
        self.height_display = self.winfo_screenheight()
        x, y = int(self.width_display / 3), int(self.height_display / 3)

        self.toplevel = tk.Toplevel()
        self.toplevel.wm_title("Nouvelle langue")
        self.toplevel.geometry(f"200x150+{x+20}+{y+20}")
        self.toplevel.resizable(False, False)
        
        self.toplevel.focus_force()
        self.toplevel.grab_set()
        

        self.lb_toplevel_new_langue = tk.Label(self.toplevel, text = "Nouvelle langue")
        self.lb_toplevel_new_langue.pack(padx = 5)

        self.sp_toplevel = ttk.Separator(self.toplevel, orient = "horizontal")
        self.sp_toplevel.pack(pady = 5, padx = 20, expand = True, fill = tk.X, anchor = "w")
        
        self.lb_toplevel_abre_lang = tk.Label(self.toplevel, text = "Abréviation : ")
        self.lb_toplevel_abre_lang.pack(anchor = "w")
        
        self.var_entry_toplevel_abre_lang.set("")
        self.entry_toplevel_abre_lang = tk.Entry(self.toplevel, textvariable = self.var_entry_toplevel_abre_lang)
        self.entry_toplevel_abre_lang.pack(padx = 5, anchor = "w")
        
        self.lb_toplevel_nom_lang = tk.Label(self.toplevel, text = "Nom : ")
        self.lb_toplevel_nom_lang.pack(padx = 5, anchor = "w")
        
        self.var_entry_toplevel_nom_lang.set("")
        self.entry_toplevel_nom_lang = tk.Entry(self.toplevel, textvariable = self.var_entry_toplevel_nom_lang)
        self.entry_toplevel_nom_lang.pack(padx = 5, anchor = "w")
        
        
        
        self.bt_toplevel_bt_valider = tk.Button(self.toplevel, text = "Valider", command = self.toplevel_valider)
        self.bt_toplevel_bt_valider.pack(side = "left", padx = 5, pady = 10, anchor = "w")
        
        self.bt_toplevel_annuler = tk.Button(self.toplevel, text = "Annuler", command = self.toplevel_annuler)
        self.bt_toplevel_annuler.pack(side = "right", padx = 5, pady = 10, anchor = "e")


    def toplevel_annuler(self) :
        self.toplevel.destroy()
        
        try :
            self.var_cbb_treeview.set(self.language[0])
            self.var_cbb_langue.set(self.language[0])
        except Exception as e :
            logger.error(msg = f"Up var : {str(e)}")

    
    def toplevel_valider(self) :
        if self.entry_toplevel_abre_lang.get() != "" and self.var_entry_toplevel_nom_lang.get() != "" :
            if self.check_verif_exist(dico_listbox_langue = self.dico_listbox_langue, entry_toplevel_abre_lang = self.entry_toplevel_abre_lang.get(), var_entry_toplevel_nom_lang = self.var_entry_toplevel_nom_lang.get() ) != True :
                f = open(os.path.join(self.path_dossier, "Langue.txt"), "a")
                string = self.entry_toplevel_abre_lang.get() + ":" + self.var_entry_toplevel_nom_lang.get() + "\n"
                f.write(string)
                f.close()
                
                self.reload_langue()
            
            else :
                tk.messagebox.showerror("Erreur", "Langue déjà enregistré !")
            
        else :
            tk.messagebox.showerror("Erreur", "Erreur formulaire !")
    
        self.toplevel.destroy()


    def reload_langue(self) :
        data = {}
        data['path_dossier'] = self.path_dossier
        data['dico_listbox_langue'] = self.dico_listbox_langue
        data['language'] = self.language
        Manage_File(self).construct("load_langue", data)


    def check_verif_exist(self, **kwargs) :
        for name, value in kwargs.items() :
            if name == "dico_listbox_langue" :
                dico_langue = value
            if name == "var_entry_toplevel_nom_lang" :
                new_langue = value
            if name == "entry_toplevel_abre_lang" :
                new_abre = value

        for old_abre, old_langue in dico_langue.items() :
            if old_abre == new_abre or old_langue == new_langue :
                return True



class Manage_File(tk.Tk) :
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.master = master
        

    def construct(self, fonction, *args) :
        
        self.attribution_variable(*args)

        if fonction == "load_init" :
            self.load_init()
        if fonction == "load_langue" :
            self.load_langue()
        if fonction == "load_dictionnaire" :
            self.load_dictionnaire()
        if fonction == "save_entry" :
            self.save_entry()

        if fonction == "load_all" :
            self.load_init()
            self.load_langue()
            self.load_dictionnaire()


    def attribution_variable(self, *args) :
        for name, value in args[0].items() :
            if name == "path_dossier" :
                self.path_dossier = value
            if name == "dico_listbox_langue" :
                self.dico_listbox_langue = value
            if name == "language" :
                self.language = value
            if name == "dico_mot" :
                self.dico_mot = value
            if name == "dico" :
                self.dico = value
            if name == "var_comment" :
                self.var_comment = value
            if name == "var_entry_mot" :
                self.var_entry_mot = value
            if name == "var_cbb_langue" :
                self.var_cbb_langue = value
            if name == "var_traduction" :
                self.var_traduction = value
            if name == "var_langage_trad" :
                self.var_langage_trad = value


    def load_init(self) :
        try :
            f = open(os.path.join(self.path_dossier, "Dico_init.txt"), "r")
            txt = f.read().split("\n")
            f.close()
        except Exception as e :
            logger.info(msg = f"Inexistant, création dico init : {str(e)}")
            f = open("Dico_init.txt", "w")
            f.close()


    def load_langue(self) :
        try :            
            f = open(os.path.join(self.path_dossier, "Langue.txt"), "r")
            txt = f.read()
            f.close()
            
            try :
                txt = txt.split("\n")
                for k in txt :
                    if k.split(":")[0] != "" :
                        k = k.split(":")
                        self.dico_listbox_langue[k[0]] = k[1]
            except Exception as e :
                logger.error(msg = f"Range Load_langue : {str(e)}")
            
        except Exception as e :
            logger.info(msg = f"Inexistant, création fichier langue : {str(e)}")
            f = open("Langue.txt", "w")
            f.close()

        
        for abre, nom in self.dico_listbox_langue.items():
            self.language.append(nom)

        self.language.append("---New---")
        

    def load_dictionnaire(self) :
        try :
            f = open(os.path.join(self.path_dossier, "Dictionnaire.txt"), "r")
            txt = f.read()
            f.close()
            
            try :
                txt = txt.split("\n\n")
                dico_id = 0
                for k in txt :
                    if k != "" :
                        self.dico_mot = {}
                        k = k.split("\n")
                        mots = k[0].split("|")
                        libelle = k[1]
                        
                        try :
                            libelle = re.sub(r"\\n", "\n", libelle)
                        except Exception as e :
                            logger.error(msg = f"Regex : {str(e)}")

                        self.dico_mot["libelle"] = [libelle]
                        self.dico_mot["langue"] = []
                        self.dico_mot["mot"] = []
                        
                        for i in mots :
                            if i != "" :
                                i = i.split(":")
                                self.dico_mot["langue"].append(i[0])
                                self.dico_mot["mot"].append(i[1])
                        
                        self.dico[dico_id] = self.dico_mot
                        dico_id += 1
                        del self.dico_mot
                
            except Exception as e :
                logger.error(msg = f"Range Load_dictionnaire : {str(e)}")
            
        except Exception as e :
            logger.info(msg = f"Inexistant, créatiion fichier Dictionnaire : {str(e)}")
            f = open("Dictionnaire.txt", "w")
            f.close()


    def save_entry(self) :
        mot_select = self.var_entry_mot
        langue_select = self.var_cbb_langue
        mot_trad = self.var_traduction
        langue_trad = self.var_langage_trad
        abre_lang = ''
        abre_trad = ''
        comment = [f"{self.var_comment!r}"][0][1:-1]
        
        for name, value in self.dico_listbox_langue.items() :
            if value == langue_select :
                abre_lang = name
            if value == langue_trad :
                abre_trad = name
        
        string = abre_lang + ":" + mot_select + "|" + abre_trad + ":" + mot_trad
        string = string + "\n" + comment
        
        f = open(os.path.join(self.path_dossier, "Dictionnaire.txt"), "a")
        f.write(string + "\n\n")
        f.close()
            


class Treeview(tk.Tk) :
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.master = master


    def construct(self, *args) :
        self.attribution_variable(*args)
        
        colonne = self.tree_colonne()
        data_ligne = self.tree_ligne()

        return colonne, data_ligne
    

    def attribution_variable(self, *args) :
        for name, value in args[0].items() :
            if name == "var_entry_search" :
                self.var_entry_search = value
            if name == "dico" :
                self.dico = value

          
    def tree_colonne(self) :
        colonne = ("fr",)
        for key, var in enumerate(self.dico.items()) :
            for name, value in var[1].items() :
                if name == "langue" :
                    for i in self.dico[key]["langue"] :
                        if colonne.count(i) == 0 :
                            colonne = colonne + (i,)
        
        return colonne
        
        
    def tree_ligne(self) :
        colonne = self.tree_colonne()
        ligne = []

        for key, var in enumerate(self.dico.items()) :
            for name, value in var[1].items() :
                if name == "mot" :
                    data_ligne = ()
                    lang_ligne = ()
                    
                    for i in range(0, len(colonne)) :
                        ind = 0
                        check_yes = 0
                        for x in self.dico[key]["langue"] :
                            if colonne[i] == x :
                                data_ligne = data_ligne + (value[ind],)
                                lang_ligne = lang_ligne + (self.dico[key]["langue"][ind],)
                                check_yes += 1
                                break
                            
                            ind += 1
                        
                        if check_yes == 0 :
                            data_ligne = data_ligne + ("",)
                            #lang_ligne = lang_ligne + (self.dico[key]["langue"][ind],)
                    
                    ligne.append(data_ligne)

        return ligne
                    
  
 
class Edit(tk.Tk) :
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.master = master
        

    def construct(self, *args) :
        self.attribution_variable(*args)
        self.tk_toplevel()


    def attribution_variable(self, *args) :
        for name, value in args[0].items() :
            if name == "dico" :
                self.dico = value
            if name == "var_comment" :
                self.var_comment = value
            if name == "var_langage_trad" :
                self.var_langage_trad = value
            if name == "var_cbb_treeview" :
                self.var_cbb_treeview = value
            if name == "var_cbb_langue" :
                self.var_cbb_langue = value
            if name == "language" :
                self.language = value
            if name == "path_dossier" :
                self.path_dossier = value
            if name == "dico_listbox_langue" :
                self.dico_listbox_langue = value
            if name == "item" :
                self.item_edit = value
            if name == "nom" :
                self.nom_item_edit = value
            if name == "nom" :
                self.dico_mot = value
            if name == "var_entry_mot" :
                self.var_entry_mot = value
            if name == "var_traduction" :
                self.var_traduction = value
            if name == "var_edit" :
                self.var_edit = value
       
        self.data = {}
        self.data["var_langage_trad"] = self.var_langage_trad
        self.data["var_cbb_treeview"] = self.var_cbb_treeview
        self.data["var_cbb_langue"] = self.var_cbb_langue
        self.data["language"] = self.language
        self.data["path_dossier"] = self.path_dossier
        self.data["dico_listbox_langue"] = self.dico_listbox_langue
        self.data["dico_mot"] = self.dico_mot
        self.data["var_entry_mot"] = self.var_entry_mot
        self.data["var_traduction"] = self.var_traduction
        self.data["var_edit"] = self.var_edit
        self.data["dico"] = self.dico

        
    def tk_toplevel(self):
        self.toplevel_cor = tk.Toplevel()
        self.toplevel_cor.wm_title("Correspondance")
        self.toplevel_cor.geometry("600x300")
        self.toplevel_cor.resizable(False, False)
        
        self.toplevel_cor.focus_force()
        self.toplevel_cor.grab_set()
        
        self.update_idletasks()
        self.frame()
    
    
    def frame(self) :
        self.toplevel_cor.focus_force()
        self.toplevel_cor.grab_set()
        
        self.frame_toplevel_cor_head = tk.Frame(self.toplevel_cor, borderwidth = 5, highlightthickness = 2, highlightbackground = "black")
        self.frame_toplevel_cor_head.pack(padx = 5, pady = 5, anchor = "w", expand = True, fill = tk.X)
        
        self.frame_toplevel_cor_body = tk.Frame(self.toplevel_cor, borderwidth = 5, highlightthickness = 2, highlightbackground = "black")
        self.frame_toplevel_cor_body.pack(side = "left", padx = 5, pady = 5,anchor = "w")
        
        self.frame_toplevel_cor_treeview = tk.Frame(self.frame_toplevel_cor_body, width = 300, height = 150)
        self.frame_toplevel_cor_treeview.pack(side = "top", anchor = "w")
        self.frame_toplevel_cor_treeview.pack_propagate(False)

        self.frame_toplevel_cor_treeview_bottom = tk.Frame(self.frame_toplevel_cor_treeview)
        self.frame_toplevel_cor_treeview_bottom.pack(side = "bottom", expand = True, fill = tk.X)
        
        self.canvas_treeview_toplevel_cor = tk.Canvas(self.frame_toplevel_cor_treeview, width = 100, height = 5)
        self.canvas_treeview_toplevel_cor.pack(side = "left")

        self.frame_toplevel_cor_body_libelle = tk.Frame(self.frame_toplevel_cor_body)
        self.frame_toplevel_cor_body_libelle.pack(side = "bottom", pady = 10)

        self.canvas_libelle = tk.Canvas(self.frame_toplevel_cor_body_libelle)
        self.canvas_libelle.pack(side = "left")

        self.frame_libelle = tk.Frame(self.frame_toplevel_cor_body_libelle)
        self.frame_libelle.pack(side = "right")

        self.frame_toplevel_cor_body_option = tk.Frame(self.toplevel_cor, borderwidth = 5, width = 100, height = 10)
        self.frame_toplevel_cor_body_option.pack(side = "left", expand = True, fill = tk.BOTH, padx = 5, pady = 5)

        self.widget()

        try :
            if self.horti_scrollbar_toplevel.winfo_exists() == 1 :
                self.horti_scrollbar_toplevel.destroy()
        except :
            pass

        try :
            self.horti_scrollbar_toplevel = ttk.Scrollbar(self.frame_toplevel_cor_treeview_bottom, orient = "horizontal")
            self.horti_scrollbar_toplevel['command'] = self.treeview_toplevel_cor.xview
            self.horti_scrollbar_toplevel.pack(expand = True, fill=tk.X, pady = 5)
            self.treeview_toplevel_cor['xscrollcommand'] = self.horti_scrollbar_toplevel.set
            
            self.treeview_toplevel_cor.config(scrollregion = self.canvas_treeview_toplevel_cor.bbox('all'))        
        
        except :
            pass


    def widget(self) :
        try :
            if self.cbb_toplevel_cor_edit.winfo_exists() == 1 :
                self.cbb_toplevel_cor_edit.destroy()
        except :
            pass

        self.lb_toplevel_cor_nom = tk.Label(self.frame_toplevel_cor_head, text = f"Mot séléctionné : '{self.nom_item_edit}'")
        self.lb_toplevel_cor_nom.grid(row = 0, column = 0)
        
        self.treeview_toplevel_cor = ttk.Treeview(self.canvas_treeview_toplevel_cor, height = 5)
        self.treeview_toplevel_cor.pack(side = "left", padx = 5, pady = 5)

        
        colonne = ()
        ligne = ()
        libelle = ""
        
        Manage_File(self).construct("load_dictionnaire", self.data)
        
        max_lenght = 0
        for key, dico in self.dico.items() :
            if key == int(self.item_edit) :
                for name, value in dico.items() :
                    if name == "langue" :
                        for k in value :
                            colonne = colonne + (k,)
                    if name == "mot" :
                        for k in value :
                            ligne = ligne + (k,)
                            len_k = len(k)
                            if len_k > max_lenght :
                                max_lenght = len_k   
                    if name == "libelle" :
                        libelle = value[0]
                        
            else :
                continue
            break
        
        ligne = ligne + ("---Nouvelle Traduction---",)
        
        self.treeview_toplevel_cor["columns"] = colonne
        self.treeview_toplevel_cor["show"] = "headings"
        
        for k in range(0, len(colonne)) :
            self.treeview_toplevel_cor.column(k, minwidth = max_lenght*8 + 20, width = 70)
            self.treeview_toplevel_cor.heading(k, text = colonne[k])
        
        self.treeview_toplevel_cor.insert("", "end", 0, values = ligne)
        
        self.txt_toplevel_cor = tk.Text(self.canvas_libelle, width = 35, height = 3, wrap = "none")
        self.txt_toplevel_cor.pack(side = "bottom", anchor = "w")
        self.txt_toplevel_cor.insert("end", libelle)
        
        self.bt_toplevel_cor_txt = tk.Button(self.frame_libelle, text = "UP", command = self.up_comment)
        self.bt_toplevel_cor_txt.pack(side = "bottom", anchor = "w", ipady = 12)
    
        self.lb_toplevel_cor_edit = tk.Label(self.frame_toplevel_cor_body_option, text = "Edit")
        self.lb_toplevel_cor_edit.grid(row = 0, column = 0)
        
        self.var_cbb_toplevel_edit = tk.StringVar()
        self.cbb_toplevel_cor_edit = ttk.Combobox(self.frame_toplevel_cor_body_option, textvariable = self.var_cbb_toplevel_edit, values = ligne, state = "readonly")
        self.cbb_toplevel_cor_edit.grid(row = 0, column = 1)
        
        self.cbb_toplevel_cor_edit.bind("<<ComboboxSelected>>", self.edition)
        
       
    def edition(self, event) :
        try : 
            if self.frame_toplevel_cor_body_option.winfo_exists() == 1 :
                for child in self.frame_toplevel_cor_body_option_edit.winfo_children() :
                    child.destroy()
                self.frame_toplevel_cor_body_option_edit.destroy()
        except :
            pass
        
        self.edition_widget()
        
    
    def edition_widget(self) :  
        self.frame_toplevel_cor_body_option_edit = tk.Frame(self.frame_toplevel_cor_body_option)
        self.frame_toplevel_cor_body_option_edit.grid(row = 1, column = 0, columnspan = 10)
    
        self.sp_toplevel_edit = ttk.Separator(self.frame_toplevel_cor_body_option_edit, orient = "horizontal")
        self.sp_toplevel_edit.grid(row = 1, column = 0, pady = 5, columnspan = 5, sticky = "we")
        
        self.lb_toplevel_cor_new_name = tk.Label(self.frame_toplevel_cor_body_option_edit, text = "Nouveau nom : ")
        self.lb_toplevel_cor_new_name.grid(row = 2, column = 0, sticky = "w")
        
        self.var_entry_toplevel_cor = tk.StringVar()
        self.entry_toplevel_cor_new_name = tk.Entry(self.frame_toplevel_cor_body_option_edit, textvariable = self.var_entry_toplevel_cor)
        self.entry_toplevel_cor_new_name.grid(row = 2, column = 1, sticky = "w")
        
        if self.var_cbb_toplevel_edit.get() == "---Nouvelle Traduction---" :
            self.lb_toplevel_cor_trad = tk.Label(self.frame_toplevel_cor_body_option_edit, text = "Traduction")
            self.lb_toplevel_cor_trad.grid(row = 4, column = 0)
            
            self.var_cbb_toplevel_edit_trad = tk.StringVar()
            self.cbb_toplevel_cor_edit_trad = ttk.Combobox(self.frame_toplevel_cor_body_option_edit, textvariable = self.var_cbb_toplevel_edit_trad, values = self.language, state = "readonly")
            self.cbb_toplevel_cor_edit_trad.grid(row = 4, column = 1)
         
            self.var_edit = True
            self.cbb_toplevel_cor_edit_trad.bind("<<ComboboxSelected>>", self.choix_treeview)
        
        self.bt_toplevel_cor_new_name = tk.Button(self.frame_toplevel_cor_body_option_edit, text = "valider", command = self.valider)
        self.bt_toplevel_cor_new_name.grid(row = 10, column = 0, sticky = "w")
         
     
    def identify_language(self, langue) :
        f = open(os.path.join(self.path_dossier, "Langue.txt"), "r")
        txt = f.read()
        f.close()
        
        txt = txt.split("\n")
        
        for k in txt :
            k = k.split(":")
            if k[1] == langue :
                abre = k[0]
                return abre
        
     
    def valider(self) :
        if self.cbb_toplevel_cor_edit.get() == "---Nouvelle Traduction---" :            
            new_mot = self.var_entry_toplevel_cor.get()
            langue = self.var_cbb_toplevel_edit_trad.get()
            langue = self.identify_language(langue)

            for iid, var in self.dico.items() :
                if iid == int(self.item_edit) :
                    if self.verif_exist_mot(new_langue = langue, dico = self.dico, new_mot = self.var_entry_toplevel_cor) != True :
                        self.dico[iid]["mot"].append(new_mot)
                        self.dico[iid]["langue"].append(langue)
                        self.save_modif()
                    else :
                        break
                    
                    try :
                        for child in self.frame_toplevel_cor_body_option.winfo_children() :
                            child.destroy()
                        for child in self.toplevel_cor.winfo_children() :
                            child.destroy()
                    except :
                        pass

                    
                    self.frame()
            
                    tk.messagebox.showinfo("Enregistré", "Traduction enregistré !")
            
        else :
            old_word = self.cbb_toplevel_cor_edit.get()
            
            find = 0
            for iid, var in self.dico.items() :
                if iid == int(self.item_edit) :
                    for k in range(0, len(var["mot"])) :
                        if old_word == var["mot"][k] :
                            self.dico[iid]["mot"][k] = str(self.var_entry_toplevel_cor.get())
                            self.save_modif()
                            find = 1
                            break
                
                        elif old_word == "" and var["mot"][k] == "" :
                            self.dico[iid]["mot"][k] = self.var_entry_toplevel_cor.get()
                            self.save_modif()
                            find = 1
                            break
            
            try :
                for child in self.frame_toplevel_cor_body_option.winfo_children() :
                    child.destroy()
                for child in self.toplevel_cor.winfo_children() :
                    child.destroy()
            except :
                pass
            
 
            self.frame()
             
        
    def save_modif(self) :
        txt = ""
        
        for key, dic in self.dico.items() :
            for k in range(0, len(dic["mot"])) :
                if k > 0 :
                    txt += "|"
                txt += dic["langue"][k]
                txt += ":"
                txt += dic["mot"][k]
            
            txt += "\n"
            txt += dic["libelle"][0]
            txt += "\n\n"        
        
        f = open(os.path.join(self.path_dossier, "Dictionnaire.txt"), "w")
        f.write(txt)
        f.close()

     
    def up_comment(self) :
        self.var_txt_toplevel_cor = self.txt_toplevel_cor.get("1.0", "end")
        self.txt_toplevel_cor.delete("1.0", "end")
        self.txt_toplevel_cor.insert("end", self.var_txt_toplevel_cor)
        self.save_comment()
    

    def save_comment(self) :
        for key, dic in self.dico.items() :
            for name, value in dic.items() :
                if name == "mot" :
                    for k in range(0, len(value)) :
                        if value[k] == self.nom_item_edit :
                            self.dico[key]["libelle"] = [[f"{self.var_txt_toplevel_cor!r}"][0][1:-1]]
                            
        self.save_modif()

    
    def bind_treeview_double_click(self, event) :
        item = self.treeview.selection()[0]
        nom = self.treeview.item(item)["values"][0]

        data = {}
        data['dico'] = self.dico
        data['var_comment'] = self.var_comment
        data['var_langage_trad'] = self.var_langage_trad
        data['var_cbb_treeview'] = self.var_cbb_treeview
        data['var_cbb_langue'] = self.var_cbb_langue
        data['language'] = self.language
        data['path_dossier'] = self.path_dossier
        data['dico_listbox_langue'] = self.dico_listbox_langue
        data['item'] = item
        data['nom'] = nom
        data["dico_mot"] = self.dico_mot
        data["var_entry_mot"] = self.var_entry_mot.get()
        data["var_traduction"] = self.var_traduction.get()
        data["var_edit"] = self.var_edit

        try :
            Edit(self).construct(data)
        except Exception as e :
            logger.critical(f"Edit crash : {str(e)}")
     

    def choix_treeview(self, event) :
        self.new = False

        if self.var_edit != True :                
            try :
                for child in self.toplevel_cor.winfo_children() :
                    child.destroy()
                self.bind_treeview_double_click(event)
            except :
                pass
                
        try :
            if self.var_cbb_toplevel_edit_trad.get() == "---New---" :
                self.new = True
        except :
            pass
        
        try :
            if self.var_langage_trad == "---New---" :
                self.new = True
        except :
            pass
        
        

        if self.new == True :
            try :
                New_Trad(self).construct(self.data)
            except Exception as e :
                logger.critical(f"New Trad crash : {str(e)}")

            self.toplevel_cor.bind("<FocusOut>", self.update_language_part1)
            self.new = False
             
        else : 
            if self.var_edit == False :
                Application.construct_treeview()
   

    def update_language_part1(self, event) :
        self.toplevel_cor.bind("<FocusIn>", self.update_language)

  
    def update_language(self, event) :
        self.language = []
        try :            
            f = open(os.path.join(self.path_dossier, "Langue.txt"), "r")
            txt = f.read()
            f.close()
            
            try :
                txt = txt.split("\n")
                for k in txt :
                    if k != "" :
                        k = k.split(":")
                        self.dico_listbox_langue[k[0]] = k[1]
            except Exception as e :
                logger.error(msg = f"Erreur, range langue : {str(e)}")
            
        except Exception as e :
            logger.info(msg = f"Update, fichier inexistant, création fichier langue : {str(e)}")
            f = open("Langue.txt", "w")
            f.close()

        
        for abre, nom in self.dico_listbox_langue.items():
            self.language.append(nom)

        self.language.append("---New---")
        self.new = False

        try :
            if self.cbb_toplevel_cor_edit_trad.winfo_exists() == 1 :
                self.cbb_toplevel_cor_edit_trad.update()
                self.cbb_toplevel_cor_edit_trad.configure(textvariable = self.var_cbb_toplevel_edit_trad, values = self.language)
        except :
            pass


    def verif_exist_mot(self, **kwargs) :
        for name, value in kwargs.items() :
            if name == "new_mot" :
                new_mot = value.get()
            if name == "dico" :
                dico = value
            if name == "new_langue" :
                new_langue = value

        old_langue = []
        for iid, dic in dico.items() :
            if int(self.item_edit) == int(iid) :
                for name, value in dic.items() :
                    if name == "langue" :
                        old_langue = value

        result = "False"
        for iid, dic in dico.items() :
            for name, value in dic.items() :
                if int(self.item_edit) == int(iid) :   
                    if name == "mot" :
                        for k in value :
                            try :
                                for old in old_langue :                                    
                                    if old != new_langue :
                                        try :
                                            if k == new_mot :
                                                result = "mot"
                                        except Exception as e :
                                            logger.error(msg = f"Echec verif exist mot : {str(e)}")
                                    
                                    elif old == new_langue :
                                        result = "langue"
                            
                            except Exception as e :
                                logger.error(msg = f"Echec verif exist langue : {str(e)}")
        if result == "mot" :
            tk.messagebox.showerror("Erreur", "Mot déja existant !")
            return True
        elif result == "langue" :
            tk.messagebox.showerror("Erreur", f"Traduction en {new_langue} déja existante !")
            return True
        elif result == "False" :
            return False
                            


class About(tk.Tk) :
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.master = master

        self.update_idletasks()
        self.width_display = self.winfo_screenwidth()
        self.height_display = self.winfo_screenheight()
        x, y = int(self.width_display / 3), int(self.height_display / 3)

        self.toplevel = tk.Toplevel()
        self.toplevel.wm_title("Information")
        self.toplevel.geometry(f"350x150+{x+20}+{y+20}")
        self.toplevel.resizable(False, False)

        self.toplevel.focus_force()
        self.toplevel.grab_set()

        self.lb_toplevel = tk.Label(self.toplevel, justify =tk.LEFT, 
        text = "Ce programme de dictionnaire à été réalisé par Dgrey IndexError,\nà la demande de mon ami et frère de coeur, le Voyageur Nu.\n\nProgramme développé sur Python avec Tkinter.\nTemps de travail : ~80h")
        self.lb_toplevel.pack(anchor = "w")






if __name__ == '__main__' :
    root = tk.Tk()
    app = Application(master=root)

    try :
        app.mainloop()
    except Exception as e :
        logger.critical(msg = f"Crash Application mainloop : {str(e)}")




