"""

"""

class Groupe:
    all_groups=[]
    def __init__(self,G,num):
        
         #G une liste de personnes qui restent ensemble ou en interaction(c'est le groupe)
         self.numero_groupe=num
         all_groups+=[G]
         
        

    def all_groups():
        #une liste de listes de tous les groupes (décrit la répartition de tous les groupes)
        return all_groups 
    def add_to_group(G,p):
        #ajouter une personne à un groupe 
        G.append(p)

    def remove_from_group(G,p):
        #supprimer une personne d'un groupe 
        G.remove(p)
    
    def nombre_groupes():
        return len(all_groups)
    
    def individus_groupe(G):
        return len(G)
#si un individu du groupe est infecté , il y'a une probabilité alpha qu'il passe l'infection à une autre personne de son groupe
#on choisit alpha=1/8
    def quel_groupe(p):
        for g in all_groups():
            if p in g :
                return g 
            
    def appartient_au_groupe(p,G):
        if p in G:
            return True 
        else:
            return False
        
    def joindre_le_combat(p,z):
        if p.strength < h.strength :
            L=hProximity(p)
            G=[]
            for h in L :
                if (appartient_au_groupe(h,quel_groupe(p))==True or h.morality=="hero") and h.fighting==False :
                    G.append(h)
            F=z.strength
            Gf=[h.strength for h in G].sort() 
            i=1
            s=Gf[0]
            T=[]
            while i<len(Gf):
                if s<F:
                    s+=Gf[i]
                for h in G :
                    if h.strength==Gf[i] :
                        T.append(h)
                i+=1
                
    
        