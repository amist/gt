import os
import math
import json
import random
import configparser

class TSPPartial(object):
    '''
    functional approach. all data is simple data structures.
    '''
    def __init__(self):
        self.cities = {}
        
        
    def create_child(self, parent1, parent2):
        child = parent1
        child += [x for x in parent2 if x not in parent1]
        return child
        
        
    def pick_merge(self, individuals_collection, population_chromosome=None):
        if population_chromosome is None:
            indexes = [-1, -1]
            min_shared = 99999
            for i in range(len(individuals_collection)-1):
                for j in range(i+1, len(individuals_collection)):
                    shared = len(set(individuals_collection[i]) & set(individuals_collection[j]))
                    if shared == 1:
                        print('returning one shared merge')
                        return [i, j]
                    if shared != 0 and shared < min_shared:
                        # print(shared)
                        min_shared = shared
                        indexes = [i, j]
            # print(min_shared)
            # print(indexes)
            assert indexes[0] != indexes[1]
            print('returning non-one shared merge')
            return indexes
        else:
            assert 'should not be in use' == ''
            index = -1
            min_shared = 99999
            for i in range(len(individuals_collection)):
                shared = len(set(individuals_collection[i]) & set(population_chromosome))
                if shared != 0 and shared < min_shared:
                    min_shared = shared
                    index = i
            return i
        
        
    def get_fitness(self, chromosome):
        dist = 0
        for i in range(len(chromosome)):
            x1, y1 = self.cities[str(chromosome[i-1])]
            x2, y2 = self.cities[str(chromosome[i])]
            dist += math.sqrt((x1 - x2) ** 2 + (y1- y2) ** 2)
        return dist
        
        
    def list_to_pieces(self, shared, c):
        indexes = sorted([c.index(x) for x in shared])
        pieces = []
        for i in range(len(indexes)):
            if i == len(indexes)-1:
                piece = c[indexes[i]:] + [c[0]]
            else:
                piece = c[indexes[i]:indexes[i+1]+1]
            # print(piece)
            pieces.append(piece)
        # print('pieces')
        # print(pieces)
        return pieces
        
        
    def glue_pieces(self, ps):
        firsts = [x[0] for x in ps]
        lasts = [x[-1] for x in ps]
        glue_points = set(firsts) & set(lasts)
        while len(glue_points) > 0:
            gp = glue_points.pop()
            candidates = [p for p in ps if p[0] == gp or p[-1] == gp]
            # print(candidates)
            # print(gp)
            c1 = candidates[0]
            c2 = candidates[1]
            ps.remove(c1)
            ps.remove(c2)
            if c1.index(gp) == 0:
                c1 = c1[::-1]
            if c2.index(gp) == len(c2)-1:
                c2 = c2[::-1]
            ps.append(c1 + c2[1:])
            firsts = [x[0] for x in ps]
            lasts = [x[-1] for x in ps]
            glue_points = set(firsts) & set(lasts)
        return ps
        
        
    def merge_pieces(self, p1, p2):
        consensus = [p for p in p1 if p in p2 or p[::-1] in p2]
        p1_leftover = [p for p in p1 if p not in consensus and p[::-1] not in consensus]
        p2_leftover = [p for p in p2 if p not in consensus and p[::-1] not in consensus]
        # print('consensus', consensus)
        # print('p1_leftover', p1_leftover)
        # print('p2_leftover', p2_leftover)
        consensus = self.glue_pieces(consensus)
        # print('consensus', consensus)
        
        paths = consensus + p1_leftover + p2_leftover
        # print('paths', paths)
        cur = random.choice(paths)[0]
        build = []
        while len(paths) > 0:
            candidates = [x for x in paths if x[0] == cur or x[-1] == cur]
            if len(candidates) == 0:
                cur = random.choice(paths)[0]
                candidates = [x for x in paths if x[0] == cur or x[-1] == cur]
            # print('cur', cur)
            # print('candidates', candidates)
            # print('paths', paths)
            chosen = random.choice(candidates)
            paths.remove(chosen)
            if cur == chosen[0]:
                cur = chosen[-1]
            elif cur == chosen[-1]:
                cur = chosen[0]
            else:
                assert False
            build += chosen
                
        
        # print('build')
        seen = set()
        seen_add = seen.add
        # print(build)
        build = [x for x in build if not (x in seen or seen_add(x))]
        # print('build 2')
        # print(build)
        return [build]
        assert False
        
        
        # print('in merge pieces')
        # print('p1, p2:', p1, p2)
        p1 = [x if x[0] < x[-1] else x[::-1] for x in p1]
        p2 = [x if x[0] < x[-1] else x[::-1] for x in p2]
        # print('p1, p2 after normalization:', p1, p2)
        
        merged = []
        shared = [x[0] for x in p1]
        # print('shared', shared)
        # for s in shared:
        # collision_resolve = 0
        for s1 in p1:
            # [s1] = [x for x in p1 if x[0] == s]
            try:
                similar_segments = [x for x in p2 if x[0] == s1[0] and x[-1] == s1[-1]]
                try:
                    s2 = similar_segments[0]
                except IndexError:
                    print('IndexError')
                    print(p1)
                    print(p2)
                    raise IndexError
                p2.pop(p2.index(s2))
                # if len(similar_segments) == 1:
                    # s2 = similar_segments[0]
                # else:
                    # s2 = similar_segments[collision_resolve]
                    # collision_resolve +=  1
                # [s2] = [x for x in p2 if x[0] == s1[0] and x[-1] == s1[-1]]
            except ValueError:
                print(p1)
                print(p2)
                print(s1)
                raise ValueError
            assert s1[-1] == s2[-1]
            # print('s1, s2:', s1, s2)
            if len(s1) == 2 and len(s2) == 2:
                merged.append(s1)
            elif len(s1) == 2 and len(s2) != 2:
                merged.append(s2)
            elif len(s1) != 2 and len(s2) == 2:
                merged.append(s1)
            else:
                mask = [0] * (len(s1)-2) + [1] * (len(s2)-2)        # skip firsts and lasts
                random.shuffle(mask)
                # print('mask:', mask)
                to_append = [s1[0]]     # similar in both segments
                i1 = i2 = 1
                # print(to_append)
                for m in mask:
                    # print(m)
                    if m == 0:
                        to_append.append(s1[i1])
                        # print(to_append)
                        i1 += 1
                    else:
                        to_append.append(s2[i2])
                        # print(to_append)
                        i2 += 1
                to_append.append(s1[-1])     # similar in both segments
                # print(to_append)
                merged.append(to_append)
                # assert 'not implemented yet' == ''
                
        # print(merged)
        return merged
            
            
    def pieces_to_list(self, ps):
        # print('pieces to list')
        # print('ps:', ps)
        
        return ps[0]
        assert False        # code below was before assuming ps is one piece
        
        
        ls = []
        p = ps.pop()        # can also be ps.pop(0)
        next_node = p[0]
        # print(p)
        l = []
        for node in p:
            l.append(node)
        ls += l[:-1]
        if next_node == p[0]:
            next_node = p[-1]
        elif next_node == p[-1]:
            next_node = p[0]
        else:
            assert False        # shouldn't be here
        while len(ps) > 0:
            # print(ps, next_node)
            [next_index] = [ps.index(x) for x in ps if x[0] == next_node or x[-1] == next_node]
            p = ps.pop(next_index)
            l = []
            for node in p:
                if node not in ls:
                    l.append(node)
            if next_node == p[0]:
                next_node = p[-1]
            elif next_node == p[-1]:
                next_node = p[0]
            else:
                assert False        # shouldn't be here
            # ls += l[:-1]
            ls += l
        return ls
        
        
    def merge(self, c1, c2):
        max_len = max(len(c1), len(c2))
        if max_len > 0.9 * len(self.cities):
            if len(c2) > len(c1):
                c1, c2 = c2, c1
                
            # make sure c2 starts with element which is also in c1
            exists = (set(c1) & set(c2)).pop()
            index = c2.index(exists)
            c2 = c2[index:] + c2[:index]
            missing = [x for x in c2 if x not in c1]
            # insert the missing according to their order at c2
            for m in missing:
                before = c2[c2.index(m)-1]
                index = c1.index(before)
                c1.insert(index, m)
                
            # TODO: add random for diversity
            return c1
        # print('in merge')
        # print(c1, c2)
        shared_set = set(c1) & set(c2)
        if len(shared_set) == 1:
            # TODO: the other way (c1 and c2 swapped)
            node = shared_set.pop()
            i1 = c1.index(node)
            i2 = c2.index(node)
            c1 = c1[i1:] + c1[:i1]
            c2 = list(reversed(c2[i2:] + c2[:i2]))
        
            # print(c1, c2)
            new_individual = [x for x in c1 if x not in c2]
            shared = self.merge_shared(c1, c2)
            new_individual += shared
            new_individual += [x for x in c2 if x not in c1]
            # print(new_individual)
            
        else:
            new_individual = []
            
            # print('c1, c2:', c1, c2)
            node = shared_set.pop()
            i1 = c1.index(node)
            i2 = c2.index(node)
            c1 = c1[i1:] + c1[:i1]
            c2 = c2[i2:] + c2[:i2]
            # print('c1, c2 after rotation:', c1, c2)
            shared = set(c1) & set(c2)
            # print('shared:', shared)
            # indexes1 = sorted([c1.index(x) for x in shared])
            # indexes2 = sorted([c2.index(x) for x in shared])
            # indexes1 = indexes1 + [-2]        # to become -1 when +1
            # indexes2 = indexes2 + [-2]        # to become -1 when +1
            # print('indexes:', indexes1, indexes2)
            pieces1 = self.list_to_pieces(shared, c1)
            pieces2 = self.list_to_pieces(shared, c2)
            # print('pieces1, pieces2:', pieces1, pieces2)
            # print('shared:', shared)
            try:
                merged = self.merge_pieces(pieces1, pieces2)
            except IndexError:
                print('in merge, IndexError')
                print(c1)
                print(c2)
                raise IndexError
            new_individual = self.pieces_to_list(merged)
            # print(c1, c2)
            # min1 = min([c1.index(x) for x in c1 if x in c2])
            # min2 = min([c2.index(x) for x in c2 if x in c1])
            # print(min1, min2)
            # c1 = c1[min1:] + c1[:min1]
            # c2 = c2[min2:] + c2[:min2]
            # print(c1, c2)
            # shared_indexes = []
            # for shared_node in shared_set:
                # shared_indexes.append([c1.index(shared_node), c2.index(shared_node)])
            # print(shared_indexes)
            
            # new_individual = []
            # i1 = 0
            # i2 = 0
            # to_append = -1
            # while i1 < len(c1) and i2 < len(c2):
                # # print(i1, i2)
                # # print(new_individual)
                # if i1 >= len(c1):
                    # i1 += 1
                    # to_append = 2
                # if i2 >= len(c2):
                    # i2 += 1
                    # to_append = 1
                # if i1 < len(c1) and i2 < len(c2):
                    # if c1[i1] in shared_set and c2[i2] not in shared_set:
                        # # i2 += 1
                        # to_append = 2
                    # elif c1[i1] not in shared_set and c2[i2] in shared_set:
                        # # i1 += 1
                        # to_append = 1
                    # elif c1[i1] in shared_set and c2[i2] in shared_set:
                        # # i1 += 1
                        # # i2 += 1
                        # to_append = 1
                    # else:       # both not in shared_set
                        # if random.randint(0,1) == 0:
                            # # i1 += 1
                            # to_append = 1
                        # else:
                            # # i2 += 1
                            # to_append = 2
                # if to_append == 1:
                    # i1 += 1
                    # new_individual.append(c1[i1])
                # else:
                    # i2 += 1
                    # new_individual.append(c2[i2])
                
            
        try:
            assert len(new_individual) == len(set(new_individual))
        except AssertionError:
            print(c1)
            print(c2)
            print(new_individual)
            raise AssertionError
        return new_individual
        
        
    def merge_shared(self, s1, s2):
        # TODO: check for opposite directions
        shared = list(set(s1) & set(s2))
        random.shuffle(shared)
        return shared
        
        
    def mutate(self, chromosome):
        a_index = random.randint(0, len(chromosome)-1)
        b_index = random.randint(0, len(chromosome)-1)
        if a_index > b_index:
            a_index, b_index = b_index, a_index
        if random.randint(0,1) == 0:
            # swap edges
            if a_index == 0:
                chromosome[a_index:b_index] = chromosome[b_index-1::-1]
            else:
                chromosome[a_index:b_index] = chromosome[b_index-1:a_index-1:-1]
        else:
            # insert node after node
            node = chromosome.pop(a_index)
            chromosome.insert(b_index, node)
            
        return chromosome