---
title: Leiden_Technique
source_path: /Users/amelie.girard/LLMKnowledgeBase/raw/papers/Leiden_Technique.pdf
source_url: null
ingested_at: '2026-05-01'
processed: true
processed_at: '2026-05-02'
---
# **From Louvain to Leiden: guaranteeing well-connected communities** 

V.A. Traag, _[∗]_ L. Waltman, and N.J. van Eck 

_Centre for Science and Technology Studies, Leiden University, the Netherlands_ 

(Dated: October 31, 2019) 

Community detection is often used to understand the structure of large and complex networks. One of the most popular algorithms for uncovering community structure is the so-called Louvain algorithm. We show that this algorithm has a major defect that largely went unnoticed until now: the Louvain algorithm may yield arbitrarily badly connected communities. In the worst case, communities may even be disconnected, especially when running the algorithm iteratively. In our experimental analysis, we observe that up to 25% of the communities are badly connected and up to 16% are disconnected. To address this problem, we introduce the Leiden algorithm. We prove that the Leiden algorithm yields communities that are guaranteed to be connected. In addition, we prove that, when the Leiden algorithm is applied iteratively, it converges to a partition in which all subsets of all communities are locally optimally assigned. Furthermore, by relying on a fast local move approach, the Leiden algorithm runs faster than the Louvain algorithm. We demonstrate the performance of the Leiden algorithm for several benchmark and real-world networks. We find that the Leiden algorithm is faster than the Louvain algorithm and uncovers better partitions, in addition to providing explicit guarantees. 

## **I. INTRODUCTION** 

In many complex networks, nodes cluster and form relatively dense groups—often called communities [1, 2]. Such a modular structure is usually not known beforehand. Detecting communities in a network is therefore an important problem. One of the best-known methods for community detection is called modularity [3]. This method tries to maximise the difference between the actual number of edges in a community and the expected number of such edges. We denote by _ec_ the actual number of edges in community _c_ . The expected number of _c_ edges can be expressed as _[K]_ 2 _m_[2][, where] _[ K][c]_[is the sum of the] degrees of the nodes in community _c_ and _m_ is the total number of edges in the network. This way of defining the expected number of edges is based on the so-called configuration model. Modularity is given by 

**==> picture [183 x 27] intentionally omitted <==**

where _γ >_ 0 is a resolution parameter [4]. Higher resolutions lead to more communities, while lower resolutions lead to fewer communities. 

Optimising modularity is NP-hard [5], and consequentially many heuristic algorithms have been proposed, such as hierarchical agglomeration [6], extremal optimisation [7], simulated annealing [4, 8] and spectral [9] algorithms. One of the most popular algorithms to optimise modularity is the so-called Louvain algorithm [10], named after the location of its authors. It was found to be one of the fastest and best performing algorithms in comparative analyses [11, 12], and it is one of the mostcited works in the community detection literature. 

Although originally defined for modularity, the Louvain algorithm can also be used to optimise other quality functions. An alternative quality function is the Constant Potts Model (CPM) [13], which overcomes some limitations of modularity. CPM is defined as 

**==> picture [176 x 27] intentionally omitted <==**

where _nc_ is the number of nodes in community _c_ . The interpretation of the resolution parameter _γ_ is quite straightforward. The parameter functions as a sort of threshold: communities should have a density of at least _γ_ , while the density between communities should be lower than _γ_ . Higher resolutions lead to more communities and lower resolutions lead to fewer communities, similarly to the resolution parameter for modularity. 

In this paper, we show that the Louvain algorithm has a major problem, for both modularity and CPM. The algorithm may yield arbitrarily badly connected communities, over and above the well-known issue of the resolution limit [14] (Section II A). Communities may even be internally disconnected. To address this important shortcoming, we introduce a new algorithm that is faster, finds better partitions and provides explicit guarantees and bounds (Section III). The new algorithm integrates several earlier improvements, incorporating a combination of smart local move [15], fast local move [16, 17] and random neighbour move [18]. We prove that the new algorithm is guaranteed to produce partitions in which all communities are internally connected. In addition, we prove that the algorithm converges to an asymptotically stable partition in which all subsets of all communities are locally optimally assigned. The quality of such an asymptotically stable partition provides an upper bound on the quality of an optimal partition. Finally, we demonstrate the excellent performance of the algorithm for several benchmark and real-world networks (Section IV). To ensure readability of the paper to the 

> _∗_ v.a.traag@cwts.leidenuniv.nl 

2 

**==> picture [200 x 241] intentionally omitted <==**

**----- Start of picture text -----**<br>
Move nodes<br>a) b)<br>Level 1<br>Aggregate<br>c) d)<br>Level 2<br>Move nodes<br>**----- End of picture text -----**<br>


FIG. 1. **Louvain algorithm** . The Louvain algorithm starts from a singleton partition in which each node is in its own community (a). The algorithm moves individual nodes from one community to another to find a partition (b). Based on this partition, an aggregate network is created (c). The algorithm then moves individual nodes in the aggregate network (d). These steps are repeated until the quality cannot be increased further. 

broadest possible audience, we have chosen to relegate all technical details to appendices. The main ideas of our algorithm are explained in an intuitive way in the main text of the paper. We name our algorithm the _Leiden algorithm_ , after the location of its authors. 

## **II. LOUVAIN ALGORITHM** 

The Louvain algorithm [10] is very simple and elegant. The algorithm optimises a quality function such as modularity or CPM in two elementary phases: (1) local moving of nodes; and (2) aggregation of the network. In the local moving phase, individual nodes are moved to the community that yields the largest increase in the quality function. In the aggregation phase, an aggregate network is created based on the partition obtained in the local moving phase. Each community in this partition becomes a node in the aggregate network. The two phases are repeated until the quality function cannot be increased further. The Louvain algorithm is illustrated in Fig. 1 and summarised in pseudo-code in Algorithm A.1 in Appendix A. 

Usually, the Louvain algorithm starts from a singleton partition, in which each node is in its own community. 

**==> picture [248 x 132] intentionally omitted <==**

**----- Start of picture text -----**<br>
a) 2 5 b) 2 5<br>3 6 3 6<br>1 4 1 4<br>0 0<br>Rest of network Rest of network<br>**----- End of picture text -----**<br>


FIG. 2. **Disconnected community.** Consider the partition shown in (a). When node 0 is moved to a different community, the red community becomes internally disconnected, as shown in (b). However, nodes 1–6 are still locally optimally assigned, and therefore these nodes will stay in the red community. 

However, it is also possible to start the algorithm from a different partition [15]. In particular, in an attempt to find better partitions, multiple consecutive iterations of the algorithm can be performed, using the partition identified in one iteration as starting point for the next iteration. 

## **A. Badly connected communities** 

We now show that the Louvain algorithm may find arbitrarily badly connected communities. In particular, we show that Louvain may identify communities that are internally disconnected. That is, one part of such an internally disconnected community can reach another part only through a path going outside the community. Importantly, the problem of disconnected communities is not just a theoretical curiosity. As we will demonstrate in Section IV, the problem occurs frequently in practice when using the Louvain algorithm. Perhaps surprisingly, iterating the algorithm aggravates the problem, even though it does increase the quality function. 

In the Louvain algorithm, a node may be moved to a different community while it may have acted as a bridge between different components of its old community. Removing such a node from its old community disconnects the old community. One may expect that other nodes in the old community will then also be moved to other communities. However, this is not necessarily the case, as the other nodes may still be sufficiently strongly connected to their community, despite the fact that the community has become disconnected. 

To elucidate the problem, we consider the example illustrated in Fig. 2. The numerical details of the example can be found in Appendix B. The thick edges in Fig. 2 represent stronger connections, while the other edges represent weaker connections. At some point, the Louvain algorithm may end up in the community structure shown 

3 

in Fig. 2(a). Nodes 0–6 are in the same community. Nodes 1–6 have connections only within this community, whereas node 0 also has many external connections. The algorithm continues to move nodes in the rest of the network. At some point, node 0 is considered for moving. When a sufficient number of neighbours of node 0 have formed a community in the rest of the network, it may be optimal to move node 0 to this community, thus creating the situation depicted in Fig. 2(b). In this new situation, nodes 2, 3, 5 and 6 have only internal connections. These nodes are therefore optimally assigned to their current community. On the other hand, after node 0 has been moved to a different community, nodes 1 and 4 have not only internal but also external connections. Nevertheless, depending on the relative strengths of the different connections, these nodes may still be optimally assigned to their current community. In that case, nodes 1–6 are all locally optimally assigned, despite the fact that their community has become disconnected. Clearly, it would be better to split up the community. Nodes 1–3 should form a community and nodes 4–6 should form another community. However, the Louvain algorithm does not consider this possibility, since it considers only individual node movements. Moreover, when no more nodes can be moved, the algorithm will aggregate the network. When a disconnected community has become a node in an aggregate network, there are no more possibilities to split up the community. Hence, the community remains disconnected, unless it is merged with another community that happens to act as a bridge. 

Obviously, this is a worst case example, showing that disconnected communities may be identified by the Louvain algorithm. More subtle problems may occur as well, causing Louvain to find communities that are connected, but only in a very weak sense. Hence, in general, Louvain may find arbitrarily badly connected communities. 

This problem is different from the well-known issue of the resolution limit of modularity [14]. Due to the resolution limit, modularity may cause smaller communities to be clustered into larger communities. In other words, modularity may “hide” smaller communities and may yield communities containing significant substructure. CPM does not suffer from this issue [13]. Nevertheless, when CPM is used as the quality function, the Louvain algorithm may still find arbitrarily badly connected communities. Hence, the problem of Louvain outlined above is independent from the issue of the resolution limit. In the case of modularity, communities may have significant substructure both because of the resolution limit and because of the shortcomings of Louvain. 

In fact, although it may seem that the Louvain algorithm does a good job at finding high quality partitions, in its standard form the algorithm provides only one guarantee: the algorithm yields partitions for which it is guaranteed that no communities can be merged. In other words, communities are guaranteed to be well separated. Somewhat stronger guarantees can be obtained by iterating the algorithm, using the partition obtained 

in one iteration of the algorithm as starting point for the next iteration. When iterating Louvain, the quality of the partitions will keep increasing until the algorithm is unable to make any further improvements. At this point, it is guaranteed that each individual node is optimally assigned. In this iterative scheme, Louvain provides two guarantees: (1) no communities can be merged and (2) no nodes can be moved. 

Contrary to what might be expected, iterating the Louvain algorithm aggravates the problem of badly connected communities, as we will also see in Section IV. This is not too difficult to explain. After the first iteration of the Louvain algorithm, some partition has been obtained. In the first step of the next iteration, Louvain will again move individual nodes in the network. Some of these nodes may very well act as bridges, similarly to node 0 in the above example. By moving these nodes, Louvain creates badly connected communities. Moreover, Louvain has no mechanism for fixing these communities. Iterating the Louvain algorithm can therefore be seen as a double-edged sword: it improves the partition in some way, but degrades it in another way. 

The problem of disconnected communities has been observed before in the context of the label propagation algorithm [19]. However, so far this problem has never been studied for the Louvain algorithm. Moreover, the deeper significance of the problem was not recognised: disconnected communities are merely the most extreme manifestation of the problem of arbitrarily badly connected communities. Trying to fix the problem by simply considering the connected components of communities [19–21] is unsatisfactory because it addresses only the most extreme case and does not resolve the more fundamental problem. We therefore require a more principled solution, which we will introduce in the next section. 

## **III. LEIDEN ALGORITHM** 

We here introduce the Leiden algorithm, which guarantees that communities are well connected. The Leiden algorithm is partly based on the previously introduced smart local move algorithm [15], which itself can be seen as an improvement of the Louvain algorithm. The Leiden algorithm also takes advantage of the idea of speeding up the local moving of nodes [16, 17] and the idea of moving nodes to random neighbours [18]. We consider these ideas to represent the most promising directions in which the Louvain algorithm can be improved, even though we recognise that other improvements have been suggested as well [22]. The Leiden algorithm consists of three phases: (1) local moving of nodes, (2) refinement of the partition and (3) aggregation of the network based on the refined partition, using the non-refined partition to create an initial partition for the aggregate network. The Leiden algorithm is considerably more complex than the Louvain algorithm. Fig. 3 provides an illustration of the algorithm. The algorithm is described in pseudo-code in 

4 

**==> picture [503 x 379] intentionally omitted <==**

**----- Start of picture text -----**<br>
Move nodes Refine<br>a) b) c)<br>Level 1<br>Aggregate<br>d) e) f)<br>Move nodes Refine<br>Level 2<br>**----- End of picture text -----**<br>


FIG. 3. **Leiden algorithm** . The Leiden algorithm starts from a singleton partition (a). The algorithm moves individual nodes from one community to another to find a partition (b), which is then refined (c). An aggregate network (d) is created based on the refined partition, using the non-refined partition to create an initial partition for the aggregate network. For example, the red community in (b) is refined into two subcommunities in (c), which after aggregation become two separate nodes in (d), both belonging to the same community. The algorithm then moves individual nodes in the aggregate network (e). In this case, refinement does not change the partition (f). These steps are repeated until no further improvements can be made. 

## Algorithm A.2 in Appendix A. 

In the Louvain algorithm, an aggregate network is created based on the partition _P_ resulting from the local moving phase. The idea of the refinement phase in the Leiden algorithm is to identify a partition _P_ refined that is a refinement of _P_ . Communities in _P_ may be split into multiple subcommunities in _P_ refined. The aggregate network is created based on the partition _P_ refined. However, the initial partition for the aggregate network is based on _P_ , just like in the Louvain algorithm. By creating the aggregate network based on _P_ refined rather than _P_ , the Leiden algorithm has more room for identifying high-quality partitions. In fact, by implementing the refinement phase in the right way, several attractive guarantees can be given for partitions produced by the Leiden 

## algorithm. 

The refined partition _P_ refined is obtained as follows. Initially, _P_ refined is set to a singleton partition, in which each node is in its own community. The algorithm then locally merges nodes in _P_ refined: nodes that are on their own in a community in _P_ refined can be merged with a different community. Importantly, mergers are performed only within each community of the partition _P_ . In addition, a node is merged with a community in _P_ refined only if both are sufficiently well connected to their community in _P_ . After the refinement phase is concluded, communities in _P_ often will have been split into multiple communities in _P_ refined, but not always. 

In the refinement phase, nodes are not necessarily greedily merged with the community that yields the 

5 

largest increase in the quality function. Instead, a node may be merged with any community for which the quality function increases. The community with which a node is merged is selected randomly (similar to [18]). The larger the increase in the quality function, the more likely a community is to be selected. The degree of randomness in the selection of a community is determined by a parameter _θ >_ 0. Randomness in the selection of a community allows the partition space to be explored more broadly. Node mergers that cause the quality function to decrease are not considered. This contrasts with optimisation algorithms such as simulated annealing, which do allow the quality function to decrease [4, 8]. Such algorithms are rather slow, making them ineffective for large networks. Excluding node mergers that decrease the quality function makes the refinement phase more efficient. As we prove in Appendix C 1, even when node mergers that decrease the quality function are excluded, the optimal partition of a set of nodes can still be uncovered. This is not the case when nodes are greedily merged with the community that yields the largest increase in the quality function. In that case, some optimal partitions cannot be found, as we show in Appendix C 2. 

Another important difference between the Leiden algorithm and the Louvain algorithm is the implementation of the local moving phase. Unlike the Louvain algorithm, the Leiden algorithm uses a fast local move procedure in this phase. Louvain keeps visiting all nodes in a network until there are no more node movements that increase the quality function. In doing so, Louvain keeps visiting nodes that cannot be moved to a different community. In the fast local move procedure in the Leiden algorithm, only nodes whose neighbourhood has changed are visited. This is similar to ideas proposed recently as “pruning” [16] and in a slightly different form as “prioritisation” [17]. The fast local move procedure can be summarised as follows. We start by initialising a queue with all nodes in the network. The nodes are added to the queue in a random order. We then remove the first node from the front of the queue and we determine whether the quality function can be increased by moving this node from its current community to a different one. If we move the node to a different community, we add to the rear of the queue all neighbours of the node that do not belong to the node’s new community and that are not yet in the queue. We keep removing nodes from the front of the queue, possibly moving these nodes to a different community. This continues until the queue is empty. For a full specification of the fast local move procedure, we refer to the pseudo-code of the Leiden algorithm in Algorithm A.2 in Appendix A. Using the fast local move procedure, the first visit to all nodes in a network in the Leiden algorithm is the same as in the Louvain algorithm. However, after all nodes have been visited once, Leiden visits only nodes whose neighbourhood has changed, whereas Louvain keeps visiting all nodes in the network. In this way, Leiden implements the local moving phase more efficiently than Louvain. 

TABLE I. Overview of the guarantees provided by the Louvain algorithm and the Leiden algorithm. 

|||Louvain|Leiden|
|---|---|---|---|
|Each|_γ_-separation|||
|iteration|_γ_-connectivity|||
|Stable|Node optimality|||
|iteration|Subpartition _γ_-density|||
|Asymptotic|Uniform _γ_-density<br>Subset optimality||<br>|



## **A. Guarantees** 

We now consider the guarantees provided by the Leiden algorithm. The algorithm is run iteratively, using the partition identified in one iteration as starting point for the next iteration. We can guarantee a number of properties of the partitions found by the Leiden algorithm at various stages of the iterative process. Below we offer an intuitive explanation of these properties. We provide the full definitions of the properties as well as the mathematical proofs in Appendix D. 

After each iteration of the Leiden algorithm, it is guaranteed that: 

1. All communities are _γ_ -separated. 

2. All communities are _γ_ -connected. 

In these properties, _γ_ refers to the resolution parameter in the quality function that is optimised, which can be either modularity or CPM. The property of _γ_ -separation is also guaranteed by the Louvain algorithm. It states that there are no communities that can be merged. The property of _γ_ -connectivity is a slightly stronger variant of ordinary connectivity. As discussed in Section II A, the Louvain algorithm does not guarantee connectivity. It therefore does not guarantee _γ_ -connectivity either. 

An iteration of the Leiden algorithm in which the partition does not change is called a stable iteration. After a stable iteration of the Leiden algorithm, it is guaranteed that: 

3. All nodes are locally optimally assigned. 

4. All communities are subpartition _γ_ -dense. 

Node optimality is also guaranteed after a stable iteration of the Louvain algorithm. It means that there are no individual nodes that can be moved to a different community. Subpartition _γ_ -density is not guaranteed by the Louvain algorithm. A community is subpartition _γ_ -dense if it can be partitioned into two parts such that: (1) the two parts are well connected to each other; (2) neither part can be separated from its community; and (3) each part is also subpartition _γ_ -dense itself. Subpartition _γ_ - density does not imply that individual nodes are locally optimally assigned. It only implies that individual nodes are well connected to their community. 

6 

TABLE II. Overview of the empirical networks and of the maximal modularity after 10 replications of 10 iterations each, both for the Louvain and for the Leiden algorithm. 

||||Max. modularity|Max. modularity|
|---|---|---|---|---|
||Nodes|Degree|Louvain|Leiden|
|DBLPa|317 080|6_._6|0_._8262|0_._8387|
|Amazona|334 863|5_._6|0_._9301|0_._9341|
|IMDBb|374 511|80_._2|0_._7062|0_._7069|
|Live Journala|3 997 962|17_._4|0_._7653|0_._7739|
|Web of Sciencec|9 811 130|21_._2|0_._7911|0_._7951|
|Web UKd|39 252 879|39_._8|0_._9796|0_._9801|



> a `https://snap.stanford.edu/data/` 

> b `https://sparse.tamu.edu/Barabasi/NotreDame_actors` 

> c Data cannot be shared due to license restrictions. 

> d `http://law.di.unimi.it/webdata/uk-2005/` 

In the case of the Louvain algorithm, after a stable iteration, all subsequent iterations will be stable as well. Hence, no further improvements can be made after a stable iteration of the Louvain algorithm. This contrasts with the Leiden algorithm. After a stable iteration of the Leiden algorithm, the algorithm may still be able to make further improvements in later iterations. In fact, when we keep iterating the Leiden algorithm, it will converge to a partition for which it is guaranteed that: 

5. All communities are uniformly _γ_ -dense. 

## 6. All communities are subset optimal. 

A community is uniformly _γ_ -dense if there are no subsets of the community that can be separated from the community. Uniform _γ_ -density means that no matter how a community is partitioned into two parts, the two parts will always be well connected to each other. Furthermore, if all communities in a partition are uniformly _γ_ -dense, the quality of the partition is not too far from optimal, as shown in Appendix E. A community is subset optimal if all subsets of the community are locally optimally assigned. That is, no subset can be moved to a different community. Subset optimality is the strongest guarantee that is provided by the Leiden algorithm. It implies uniform _γ_ -density and all the other above-mentioned properties. 

An overview of the various guarantees is presented in Table I. 

performance of the two algorithms in practice[1] . All experiments were run on a computer with 64 Intel Xeon E5-4667v3 2GHz CPUs and 1TB internal memory. In all experiments reported here, we used a value of 0 _._ 01 for the parameter _θ_ that determines the degree of randomness in the refinement phase of the Leiden algorithm. However, values of _θ_ within a range of roughly [0 _._ 0005 _,_ 0 _._ 1] all provide reasonable results, thus allowing for some, but not too much randomness. We use six empirical networks in our analysis. These are the same networks that were also studied in an earlier paper introducing the smart local move algorithm [15]. Table II provides an overview of the six networks. First, we show that the Louvain algorithm finds disconnected communities, and more generally, badly connected communities in the empirical networks. Second, to study the scaling of the Louvain and the Leiden algorithm, we use benchmark networks, allowing us to compare the algorithms in terms of both computational time and quality of the partitions. Finally, we compare the performance of the algorithms on the empirical networks. We find that the Leiden algorithm commonly finds partitions of higher quality in less time. The difference in computational time is especially pronounced for larger networks, with Leiden being up to 20 times faster than Louvain in empirical networks. 

## **A. Badly connected communities** 

We study the problem of badly connected communities when using the Louvain algorithm for several empirical networks. For each community in a partition that was uncovered by the Louvain algorithm, we determined whether it is internally connected or not. In addition, to analyse whether a community is badly connected, we ran the Leiden algorithm on the subnetwork consisting of all nodes belonging to the community.[2] The Leiden algorithm was run until a stable iteration was obtained. When the Leiden algorithm found that a community could be split into multiple subcommunities, we counted the community as badly connected. Note that if Leiden finds subcommunities, splitting up the community is guaranteed to increase modularity. Conversely, if Leiden does not find subcommunities, there is no guarantee that modularity cannot be increased by splitting up the community. Hence, by counting the number of communities that have been split up, we obtained a lower bound on the number of communities that are badly connected. The 

## **IV. EXPERIMENTAL ANALYSIS** 

In the previous section, we showed that the Leiden algorithm guarantees a number of properties of the partitions uncovered at different stages of the algorithm. We also suggested that the Leiden algorithm is faster than the Louvain algorithm, because of the fast local move approach. In this section, we analyse and compare the 

> 1 We implemented both algorithms in Java, available from github.com/CWTSLeiden/networkanalysis and deposited at Zenodo [23]. Additionally, we implemented a Python package, available from github.com/vtraag/leidenalg and deposited at Zenodo [24]. 

> 2 We ensured that modularity optimisation for the subnetwork was fully consistent with modularity optimisation for the whole network [13]. 

7 

**==> picture [239 x 234] intentionally omitted <==**

**----- Start of picture text -----**<br>
Disconnected (Louvain) Badly connected (Louvain)<br>Badly connected (Leiden)<br>DBLP Amazon<br>30<br>25<br>20<br>15<br>10<br>5<br>0<br>IMDB Live Journal<br>5<br>0<br>Web of Science Web UK (2005)<br>25<br>20<br>15<br>10<br>5<br>0<br>1 2 3 4 1 2 3 4<br>Iterations<br>communities<br>%<br>**----- End of picture text -----**<br>


FIG. 4. **Badly connected communities** . Percentage of communities found by the Louvain algorithm that are either disconnected or badly connected compared to percentage of badly connected communities found by the Leiden algorithm. Note that communities found by the Leiden algorithm are guaranteed to be connected. 

count of badly connected communities also included disconnected communities. For each network, we repeated the experiment 10 times. We used modularity with a resolution parameter of _γ_ = 1 for the experiments. 

As can be seen in Fig. 4, in the first iteration of the Louvain algorithm, the percentage of badly connected communities can be quite high. For the Amazon, DBLP and Web UK networks, Louvain yields on average respectively 23%, 16% and 14% badly connected communities. The percentage of disconnected communities is more limited, usually around 1%. However, in the case of the Web of Science network, more than 5% of the communities are disconnected in the iteration. 

Later iterations of the Louvain algorithm only aggravate the problem of disconnected communities, even though the quality function (i.e. modularity) increases. The second iteration of Louvain shows a large increase in the percentage of disconnected communities. In subsequent iterations, the percentage of disconnected communities remains fairly stable. The increase in the percentage of disconnected communities is relatively limited for the Live Journal and Web of Science networks. Other networks show an almost tenfold increase in the percentage of disconnected communities. The percentage of disconnected communities even jumps to 16% for the DBLP network. The percentage of badly connected communities is less affected by the number of iterations of the Louvain algorithm. Presumably, many of the badly connected communities in the iteration of Louvain be- 

come disconnected in the second iteration. Indeed, the percentage of disconnected communities becomes more comparable to the percentage of badly connected communities in later iterations. Nonetheless, some networks still show large differences. For example, after four iterations, the Web UK network has 8% disconnected communities, but twice as many badly connected communities. Even worse, the Amazon network has 5% disconnected communities, but 25% badly connected communities. 

The above results shows that the problem of disconnected and badly connected communities is quite pervasive in practice. Because the percentage of disconnected communities in the first iteration of the Louvain algorithm usually seems to be relatively low, the problem may have escaped attention from users of the algorithm. However, focussing only on disconnected communities masks the more fundamental issue: Louvain finds arbitrarily badly connected communities. The high percentage of badly connected communities attests to this. Besides being pervasive, the problem is also sizeable. In the worst case, almost a quarter of the communities are badly connected. This may have serious consequences for analyses based on the resulting partitions. For example, nodes in a community in biological or neurological networks are often assumed to share similar functions or behaviour [25]. However, if communities are badly connected, this may lead to incorrect attributions of shared functionality. Similarly, in citation networks, such as the Web of Science network, nodes in a community are usually considered to share a common topic [26, 27]. Again, if communities are badly connected, this may lead to incorrect inferences of topics, which will affect bibliometric analyses relying on the inferred topics. In short, the problem of badly connected communities has important practical consequences. 

The Leiden algorithm has been specifically designed to address the problem of badly connected communities. Fig. 4 shows how well it does compared to the Louvain algorithm. The Leiden algorithm guarantees all communities to be connected, but it may yield badly connected communities. In terms of the percentage of badly connected communities in the first iteration, Leiden performs even worse than Louvain, as can be seen in Fig. 4. Crucially, however, the percentage of badly connected communities decreases with each iteration of the Leiden algorithm. Starting from the second iteration, Leiden outperformed Louvain in terms of the percentage of badly connected communities. In fact, if we keep iterating the Leiden algorithm, it will converge to a partition without any badly connected communities, as discussed in Section III. Hence, the Leiden algorithm effectively addresses the problem of badly connected communities. 

## **B. Benchmark networks** 

To study the scaling of the Louvain and the Leiden algorithm, we rely on a variant of a well-known approach 

8 

**==> picture [474 x 180] intentionally omitted <==**

**----- Start of picture text -----**<br>
Louvain Leiden<br>µ  = 0.2 µ  = 0.4 µ  = 0.6 µ  = 0.8<br>0.8 0.6 0.4<br>0.26<br>0.78 0.58<br>0.38<br>0.24<br>0.76 0.56<br>0.36<br>0.74 0.54 0.22<br>0.34<br>10 [3] 10 [3] 10 [5]<br>10 [3]<br>10 [1] 10 [1] 10 [2]<br>10 [1]<br>10 [−] [1] 10 [−] [1] 10 [−] [1] 10 [−] [1]<br>10 [3] 10 [5] 10 [7] 10 [3] 10 [5] 10 [7] 10 [3] 10 [5] 10 [7] 10 [3] 10 [5] 10 [7]<br>Nodes<br>Quality<br>(s)<br>Time<br>**----- End of picture text -----**<br>


FIG. 5. **Scaling of benchmark results for network size** . Speed and quality of the Louvain and the Leiden algorithm for benchmark networks of increasing size (two iterations). For larger networks and higher values of _µ_ , Louvain is much slower than Leiden. For higher values of _µ_ , Leiden finds better partitions than Louvain. 

**==> picture [482 x 199] intentionally omitted <==**

**----- Start of picture text -----**<br>
Louvain Leiden<br>µ  = 0.2 µ  = 0.4 µ  = 0.6 µ  = 0.8<br>0.7974 0.4 0.21<br>0.597<br>0.79735 0.38 0.208<br>0.36 0.206<br>0.7973 0.596<br>0.34 0.204<br>0.79725 0.595 0.32 0.202<br>20 40 60 80 100 40 60 80 100 120 100 200 300 10 [2] 10 [3]<br>0.80034 0.6005 0.4 0.208<br>0.80032 0.38<br>0.6 0.206<br>0.8003 0.36<br>0.5995<br>0.80028 0.34 0.204<br>0.80026 0.599 0.32<br>500 1,000 500 1,000 1,500 1,0002,0003,0004,000 10 [3] 10 [4]<br>Time (s)<br>6<br>= 10<br>n<br>Quality<br>7<br>= 10<br>n<br>**----- End of picture text -----**<br>


FIG. 6. **Runtime versus quality for benchmark networks** . Speed and quality for the first 10 iterations of the Louvain and the Leiden algorithm for benchmark networks ( _n_ = 10[6] and _n_ = 10[7] ). The horizontal axis indicates the cumulative time taken to obtain the quality indicated on the vertical axis. Each point corresponds to a certain iteration of an algorithm, with results averaged over 10 experiments. In general, Leiden is both faster than Louvain and finds better partitions. 

for constructing benchmark networks [28]. We generated benchmark networks in the following way. First, we created a specified number of nodes and we assigned each node to a community. Communities were all of equal size. A community size of 50 nodes was used for the results presented below, but larger community sizes yielded qualitatively similar results. We then created a certain number of edges such that a specified average degree _⟨k⟩_ was obtained. For the results reported below, the average degree was set to _⟨k⟩_ = 10. Edges were created in such a way that an edge fell between two communities with a 

probability _µ_ and within a community with a probability 1 _− µ_ . We applied the Louvain and the Leiden algorithm to exactly the same networks, using the same seed for the random number generator. For both algorithms, 10 iterations were performed. We used the CPM quality function. The value of the resolution parameter was determined based on the so-called mixing parameter _µ_ [13]. We generated networks with _n_ = 10[3] to _n_ = 10[7] nodes. For each set of parameters, we repeated the experiment 10 times. Below, the quality of a partition is reported as _H_[where] _[H]_[is][defined][in][Eq.][(][2][)][and] _[m]_[is][the][number] 2 _m_[,] 

9 

**==> picture [241 x 151] intentionally omitted <==**

**----- Start of picture text -----**<br>
Louvain<br>10 [5]<br>10 [4]<br>10 [3]<br>Leiden<br>10 [2]<br>0.2 0.4 0.6 0.8<br>µ<br>(s)<br>Time<br>**----- End of picture text -----**<br>


FIG. 7. **Scaling of benchmark results for difficulty of the partition** . Speed of the first iteration of the Louvain and the Leiden algorithm for benchmark networks with increasingly difficult partitions ( _n_ = 10[7] ). In the most difficult case ( _µ_ = 0 _._ 9), Louvain requires almost 2 _._ 5 days, while Leiden needs fewer than 10 minutes. 

of edges. 

As shown in Fig. 5, for lower values of _µ_ the partition is well defined, and neither the Louvain nor the Leiden algorithm has a problem in determining the correct partition in only two iterations. Hence, for lower values of _µ_ , the difference in quality is negligible. However, as _µ_ increases, the Leiden algorithm starts to outperform the Louvain algorithm. The differences are not very large, which is probably because both algorithms find partitions for which the quality is close to optimal, related to the issue of the degeneracy of quality functions [29]. 

The Leiden algorithm is clearly faster than the Louvain algorithm. For lower values of _µ_ , the correct partition is easy to find and Leiden is only about twice as fast as Louvain. However, for higher values of _µ_ , Leiden becomes orders of magnitude faster than Louvain, reaching 10–100 times faster runtimes for the largest networks. As can be seen in Fig. 7, whereas Louvain becomes much slower for more difficult partitions, Leiden is much less affected by the difficulty of the partition. 

Fig. 6 presents total runtime versus quality for all iterations of the Louvain and the Leiden algorithm. As can be seen in the figure, Louvain quickly reaches a state in which it is unable to find better partitions. On the other hand, Leiden keeps finding better partitions, especially for higher values of _µ_ , for which it is more difficult to identify good partitions. A number of iterations of the Leiden algorithm can be performed before the Louvain algorithm has finished its first iteration. Later iterations of the Louvain algorithm are very fast, but this is only because the partition remains the same. With one exception ( _µ_ = 0 _._ 2 and _n_ = 10[7] ), all results in Fig. 6 show that Leiden outperforms Louvain in terms of both computational time and quality of the partitions. 

**==> picture [234 x 221] intentionally omitted <==**

**----- Start of picture text -----**<br>
10,000<br>Louvain<br>Leiden<br>1,000<br>100<br>10<br>1<br>DBLP Amazon IMDB Journal Science (2005)<br>of UK<br>Live<br>Web Web<br>(s)<br>Time<br>**----- End of picture text -----**<br>


FIG. 8. **First iteration runtime for empirical networks** . Speed of the first iteration of the Louvain and the Leiden algorithm for six empirical networks. Leiden is faster than Louvain especially for larger networks. 

## **C. Empirical networks** 

Analyses based on benchmark networks have only a limited value because these networks are not representative of empirical real-world networks. In particular, benchmark networks have a rather simple structure. Empirical networks show a much richer and more complex structure. We now compare how the Leiden and the Louvain algorithm perform for the six empirical networks listed in Table II. Our analysis is based on modularity with resolution parameter _γ_ = 1. For each network, Table II reports the maximal modularity obtained using the Louvain and the Leiden algorithm. 

As can be seen in Fig. 8, the Leiden algorithm is significantly faster than the Louvain algorithm also in empirical networks. In the first iteration, Leiden is roughly 2–20 times faster than Louvain. The speed difference is especially large for larger networks. This is similar to what we have seen for benchmark networks. For the Amazon and IMDB networks, the first iteration of the Leiden algorithm is only about 1 _._ 6 times faster than the first iteration of the Louvain algorithm. However, Leiden is more than 7 times faster for the Live Journal network, more than 11 times faster for the Web of Science network and more than 20 times faster for the Web UK network. In fact, for the Web of Science and Web UK networks, Fig. 9 shows that more than 10 iterations of the Leiden algorithm can be performed before the Louvain algorithm has its iteration. 

As shown in Fig. 9, the Leiden algorithm also performs better than the Louvain algorithm in terms of the qual- 

10 

ity of the partitions that are obtained. For all networks, Leiden identifies substantially better partitions than Louvain. Louvain quickly converges to a partition and is then unable to make further improvements. In contrast, Leiden keeps finding better partitions in each iteration. 

The quality improvement realised by the Leiden algorithm relative to the Louvain algorithm is larger for empirical networks than for benchmark networks. Hence, the complex structure of empirical networks creates an even stronger need for the use of the Leiden algorithm. Leiden keeps finding better partitions for empirical networks also after the first 10 iterations of the algorithm. This contrasts to benchmark networks, for which Leiden often converges after a few iterations. For empirical networks, it may take quite some time before the Leiden algorithm reaches its first stable iteration. As can be seen in Fig. 10, for the IMDB and Amazon networks, Leiden reaches a stable iteration relatively quickly, presumably because these networks have a fairly simple community structure. The DBLP network is somewhat more challenging, requiring almost 80 iterations on average to reach a stable iteration. The Web of Science network is the most difficult one. For this network, Leiden requires over 750 iterations on average to reach a stable iteration. Importantly, the first iteration of the Leiden algorithm is the most computationally intensive one, and subsequent iterations are faster. For example, for the Web of Science network, the first iteration takes about 110–120 seconds, 

- [1] S. Fortunato, Phys. Rep. **486** , 75 (2010). 

- [2] M. A. Porter, J.-P. Onnela, and P. J. Mucha, Not. AMS **56** , 1082 (2009). 

- [3] M. E. J. Newman and M. Girvan, Phys. Rev. E **69** , 026113 (2004). 

- [4] J. Reichardt and S. Bornholdt, Phys. Rev. E **74** , 016110 (2006). 

- [5] U. Brandes, D. Delling, M. Gaertler, R. Gorke, M. Hoefer, Z. Nikoloski, D. Wagner, R. G, M. Hoefer, Z. Nikoloski, and D. Wagner, IEEE Trans. Knowl. Data Eng. **20** , 172 (2008). 

- [6] A. Clauset, M. E. J. Newman, and C. Moore, Phys. Rev. E **70** , 066111 (2004). 

- [7] J. Duch and A. Arenas, Phys. Rev. E **72** , 027104 (2005). 

- [8] R. Guimerà and L. A. Nunes Amaral, Nature **433** , 895 (2005). 

- [9] M. E. J. Newman, Phys. Rev. E **74** , 036104 (2006). 

- [10] V. D. Blondel, J.-L. Guillaume, R. Lambiotte, and E. Lefebvre, J. Stat. Mech. Theory Exp. **10008** , 6 (2008). 

- [11] A. Lancichinetti and S. Fortunato, Phys. Rev. E **80** , 056117 (2009). 

- [12] Z. Yang, R. Algesheimer, and C. J. Tessone, Sci. Rep. **6** , 30750 (2016). 

- [13] V. A. Traag, P. Van Dooren, and Y. Nesterov, Phys. Rev. E **84** , 016114 (2011). 

- [14] S. Fortunato and M. Barthélemy, Proc. Natl. Acad. Sci. U. S. A. **104** , 36 (2007). 

while subsequent iterations require about 40 seconds. 

## **V. DISCUSSION** 

Community detection is an important task in the analysis of complex networks. Finding communities in large networks is far from trivial: algorithms need to be fast, but they also need to provide high-quality results. One of the most widely used algorithms is the Louvain algorithm [10], which is reported to be among the fastest and best performing community detection algorithms [11, 12]. However, as shown in this paper, the Louvain algorithm has a major shortcoming: the algorithm yields communities that may be arbitrarily badly connected. Communities may even be disconnected. 

To overcome the problem of arbitrarily badly connected communities, we introduced a new algorithm, which we refer to as the Leiden algorithm. This algorithm provides a number of explicit guarantees. In particular, it yields communities that are guaranteed to be connected. Moreover, when the algorithm is applied iteratively, it converges to a partition in which all subsets of all communities are guaranteed to be locally optimally assigned. In practical applications, the Leiden algorithm convincingly outperforms the Louvain algorithm, both in terms of speed and in terms of quality of the results, as shown by the experimental analysis presented in this paper. We conclude that the Leiden algorithm is strongly preferable to the Louvain algorithm. 

- [15] L. Waltman and N. J. van Eck, Eur. Phys. J. B **86** , 471 (2013). 

- [16] N. Ozaki, H. Tezuka, and M. Inaba, Int. J. Comput. Electr. Eng. **8** , 207 (2016). 

- [17] S. Bae, D. Halperin, J. D. West, M. Rosvall, and B. Howe, ACM Trans. Knowl. Discov. Data **11** , 1 (2017). 

- [18] V. A. Traag, Phys. Rev. E **92** , 032801 (2015). 

- [19] U. Raghavan, R. Albert, and S. Kumara, Phys. Rev. E **76** , 036106 (2007). 

- [20] M. D. Luecken, _Application of multi-resolution partitioning of interaction networks to the study of complex disease_ , Ph.D. thesis, University of Oxford (2016). 

- [21] F. A. Wolf, F. Hamey, M. Plass, J. Solana, J. S. Dahlin, B. Gottgens, N. Rajewsky, L. Simon, and F. J. Theis, bioRxiv (2018), 10.1101/208819. 

- [22] R. Rotta and A. Noack, J. Exp. Algorithmics **16** , 2.1 (2011). 

- [23] V. A. Traag, L. Waltman, and N. J. van Eck, “networkanalysis,” Zenodo, 10.5281/zenodo.1466831 (2018), Source Code. 

- [24] V. A. Traag, “leidenalg 0.7.0,” Zenodo, 10.5281/zenodo.1469357 (2018), Source Code. 

- [25] E. Bullmore and O. Sporns, Nat. Rev. Neurosci. **10** , 186 (2009). 

- [26] L. Waltman and N. J. van Eck, J. Am. Soc. Inf. Sci. Technol. **63** , 2378 (2012). 

- [27] R. Klavans and K. W. Boyack, J. Assoc. Inf. Sci. Technol. 

11 

**==> picture [241 x 304] intentionally omitted <==**

**----- Start of picture text -----**<br>
Louvain Leiden<br>DBLP Amazon<br>0.934<br>0.835 0.932<br>0.83 0.93<br>0.928<br>0.825<br>0.926<br>1 2 3 4 1 2 3 4<br>IMDB Live Journal<br>0.704 0.77<br>0.702<br>0.76<br>0.7<br>0.698<br>0.75<br>10 20 100 200<br>Web of Science Web UK<br>0.79 0.98<br>0.785 0.9798<br>0.78 0.9796<br>0.9794<br>0.775<br>1,000 2,000 2,000 4,000<br>Time (s) Time (s)<br>Quality<br>Quality<br>Quality<br>**----- End of picture text -----**<br>


FIG. 9. **Runtime versus quality for empirical networks** . Speed and quality for the first 10 iterations of the Louvain and the Leiden algorithm for six empirical networks. The horizontal axis indicates the cumulative time taken to obtain the quality indicated on the vertical axis. Each point corresponds to a certain iteration of an algorithm, with results averaged over 10 experiments. Leiden is both faster than Louvain and finds better partitions. 

**==> picture [243 x 224] intentionally omitted <==**

**----- Start of picture text -----**<br>
1,000<br>300<br>100<br>30<br>DBLP Amazon IMDB Journal Science (2005)<br>of UK<br>Live<br>Web Web<br>stability<br>until<br>iterations<br>No.<br>**----- End of picture text -----**<br>


FIG. 10. **Number of iterations until stability** . Number of iterations before the Leiden algorithm has reached a stable iteration for six empirical networks. In a stable iteration, the partition is guaranteed to be node optimal and subpartition _γ_ -dense. 

## **AUTHOR CONTRIBUTIONS STATEMENT** 

All authors conceived the algorithm and contributed to the source code. VAT performed the experimental analysis. VAT and LW wrote the manuscript. NJvE reviewed the manuscript. 

## **ADDITIONAL INFORMATION** 

**68** , 984 (2017). 

- [28] A. Lancichinetti, S. Fortunato, and F. Radicchi, Phys. Rev. E **78** , 046110 (2008). 

- [29] B. H. Good, Y. A. De Montjoye, and A. Clauset, Phys. Rev. E **81** , 046106 (2010). 

## **Competing interests** 

The authors act as bibliometric consultants to CWTS B.V., which makes use of community detection algorithms in commercial products and services. 

- [30] V. A. Traag and J. Bruggeman, Phys. Rev. E **80** , 036115 (2009). 

- [31] T. N. Dinh, X. Li, and M. T. Thai, in _2015 IEEE Int. Conf. Data Min._ (IEEE, 2015) pp. 101–110. 

## **ACKNOWLEDGMENTS** 

We gratefully acknowledge computational facilities provided by the LIACS Data Science Lab Computing Facilities through Frank Takes. We thank Lovro Subelj for his[˘] comments on an earlier version of this paper. 

12 

## **Appendix A: Pseudo-code and mathematical notation** 

Pseudo-code for the Louvain algorithm and the Leiden algorithm is provided in Algorithms A.1 and A.2, respectively. Below we discuss the mathematical notation that is used in the pseudo-code and also in the mathematical results presented in Appendices C, D, and E. There are some uncommon elements in the notation. In particular, the idea of sets of sets plays an important role, and some concepts related to this idea need to be introduced. 

Let _G_ = ( _V, E_ ) be a graph with _n_ = _|V |_ nodes and _m_ = _|E|_ edges. Graphs are assumed to be undirected. With the exception of Theorem 14 in Appendix E, the mathematical results presented in this paper apply to both unweighted and weighted graphs. For simplicity, our mathematical notation assumes graphs to be unweighted, although the notation does allow for multigraphs. A partition _P_ = _{C_ 1 _, . . . , Cr}_ consists of _r_ = _|P|_ communities, where each community _Ci ⊆ V_ consists of a set of nodes such that _V_ =[�] _i[C][i]_[and] _[C][i][ ∩][C][j]_[=] _[ ∅]_[for][all] _[i][ ̸]_[=] _[ j]_[.][For][two][sets] _[R]_[and] _S_ , we sometimes use _R_ + _S_ to denote the union _R ∪ S_ and _R − S_ to denote the difference _R \ S_ . 

A quality function _H_ ( _G, P_ ) assigns a “quality” to a partition _P_ of a graph _G_ . We aim to find a partition with the highest possible quality. The graph _G_ is often clear from the context, and we therefore usually write _H_ ( _P_ ) instead of _H_ ( _G, P_ ). Based on partition _P_ , graph _G_ can be _aggregated_ into a new graph _G[′]_ . Graph _G_ is then called the _base graph_ , while graph _G[′]_ is called the _aggregate graph_ . The nodes of the aggregate graph _G[′]_ are the communities in the partition _P_ of the base graph _G_ , i.e. _V_ ( _G[′]_ ) = _P_ . The edges of the aggregate graph _G[′]_ are multi-edges. The number of edges between two nodes in the aggregate graph _G[′]_ equals the number of edges between nodes in the two corresponding communities in the base graph _G_ . Hence, _E_ ( _G[′]_ ) = _{_ ( _C, D_ ) _|_ ( _u, v_ ) _∈ E_ ( _G_ ) _, u ∈ C ∈ P, v ∈ D ∈ P}_ , where _E_ ( _G[′]_ ) is a multiset. A quality function must have the property that _H_ ( _G, P_ ) = _H_ ( _G[′] , P[′]_ ), where _P[′]_ = _{{v} | v ∈ V_ ( _G[′]_ ) _}_ denotes the singleton partition of the aggregate graph _G[′]_ . This ensures that a quality function gives consistent results for base graphs and aggregate graphs. 

We denote by _P_ ( _v �→ C_ ) the partition that is obtained when we start from partition _P_ and we then move node _v_ to community _C_ . We write ∆ _HP_ ( _v �→ C_ ) for the change in the quality function by moving node _v_ to community _C_ for some partition _P_ . In other words, ∆ _HP_ ( _v �→ C_ ) = _H_ ( _P_ ( _v �→ C_ )) _− H_ ( _P_ ). We usually leave the partition _P_ implicit and simply write ∆ _H_ ( _v �→ C_ ). Similarly, we denote by ∆ _HP_ ( _S �→ C_ ) the change in the quality function by moving a set of nodes _S_ to community _C_ . An empty community is denoted by _∅_ . Hence, ∆ _HP_ ( _S �→∅_ ) is the change in the quality function by moving a set of nodes _S_ to an empty (i.e. new) community. 

Now consider a community _C_ that consists of two parts _S_ 1 and _S_ 2 such that _C_ = _S_ 1 _∪ S_ 2 and _S_ 1 _∩ S_ 2 = _∅_ . Suppose that _S_ 1 and _S_ 2 are disconnected. In other words, there are no edges between nodes in _S_ 1 and _S_ 2. We then require a quality function to have the property that ∆ _H_ ( _S_ 1 _�→∅_ ) _>_ 0 and ∆ _H_ ( _S_ 2 _�→∅_ ) _>_ 0. This guarantees that a partition can always be improved by splitting a community into its connected components. This comes naturally for most definitions of a community, but this is not the case when considering for example negative links [30]. 

Because nodes in an aggregate graph are sets themselves, it is convenient to define some recursive properties. 

**Definition 1.** The _recursive size_ of a set _S_ is defined as 

**==> picture [287 x 23] intentionally omitted <==**

where _∥s∥_ = 1 if _s_ is not a set itself. The _flattening_ operation for a set _S_ is defined as 

**==> picture [298 x 23] intentionally omitted <==**

where flat( _s_ ) = _s_ if _s_ is not a set itself. A set that has been flattened is called a _flat set_ . 

The recursive size of a set corresponds to the usual definition of set size in case the elements of a set are not sets themselves, but it generalizes this definition whenever the elements are sets themselves. For example, if _S_ = _{{a, b}, {c}, {d, e, f }}_ , then 

**==> picture [196 x 38] intentionally omitted <==**

This contrasts with the traditional size of a set, which is _|S|_ = 3, because _S_ contains 3 elements. The fact that the elements are sets themselves plays no role in the traditional size of a set. The flattening of _S_ is 

**==> picture [204 x 40] intentionally omitted <==**

13 

Note that _∥S∥_ = _|_ flat( _S_ ) _|_ . 

**Definition 2.** The _flattening_ operation for a partition _P_ is defined as 

**==> picture [318 x 11] intentionally omitted <==**

Hence, flat _[∗]_ ( _P_ ) denotes the operation in which each community _C ∈ P_ is flattened. A partition that has been flattened is called a _flat partition_ . 

For any partition of an aggregate graph, the equivalent partition of the base graph can be obtained by applying the flattening operation. 

Additionally, we need some terminology to describe the connectivity of communities. 

**Definition 3.** Let _G_ = ( _V, E_ ) be a graph, and let _P_ be a partition of _G_ . Furthermore, let _H_ ( _C_ ) be the subgraph induced by a community _C ∈ P_ , i.e. _V_ ( _H_ ) = _C_ and _E_ ( _H_ ) = _{_ ( _u, v_ ) _|_ ( _u, v_ ) _∈ E_ ( _G_ ) _, u, v ∈ C}_ . A community _C ∈ P_ is called _connected_ if _H_ ( _C_ ) is a connected graph. Conversely, a community _C ∈ P_ is called _disconnected_ if _H_ ( _C_ ) is a disconnected graph. 

The mathematical proofs presented in this paper rely on the Constant Potts Model (CPM) [13]. This quality function has important advantages over modularity. In particular, unlike modularity, CPM does not suffer from the problem of the resolution limit [13, 14]. Moreover, our mathematical definitions and proofs are quite elegant when expressed in terms of CPM. The CPM quality function is defined as 

**==> picture [340 x 28] intentionally omitted <==**

where _E_ ( _C, D_ ) = _|{_ ( _u, v_ ) _∈ E_ ( _G_ ) _| u ∈ C, v ∈ D}|_ denotes the number of edges between nodes in communities _C_ and _D_ . Note that this definition can also be used for aggregate graphs because _E_ ( _G_ ) is a multiset. 

The mathematical results presented in this paper also extend to modularity, although the formulations are less elegant. Results for modularity are straightforward to prove by redefining the recursive size _∥S∥_ of a set _S_ . We need to define the size of a node _v_ in the base graph as _∥v∥_ = _kv_ instead of _∥v∥_ = 1, where _kv_ is the degree of node _v_ . Furthermore, we need to rescale the resolution parameter _γ_ by 2 _m_ . Modularity can then be written as 

**==> picture [346 x 28] intentionally omitted <==**

Note that, in addition to the overall multiplicative factor of 21 _m_[,][this adds a constant] 2 _γm_ � _C ∥C_ 2 _∥_ = _[γ]_ 2[to the ordinary] definition of modularity [3]. However, this does not matter for optimisation or for the proofs. 

As discussed in the main text, the Louvain and the Leiden algorithm can be _iterated_ by performing multiple consecutive iterations of the algorithm, using the partition identified in one iteration as starting point for the next iteration. In this way, a sequence of partitions _P_ 0 _, P_ 1 _, . . ._ is obtained such that _Pt_ +1 = Louvain( _G, Pt_ ) or _Pt_ +1 = Leiden( _G, Pt_ ). The initial partition _P_ 0 usually is the singleton partition of the graph _G_ , i.e. _P_ 0 = _{{v} | v ∈ V }_ . 

## **Appendix B: Disconnected communities in the Louvain algorithm** 

In this appendix, we analyse the problem that communities obtained using the Louvain algorithm may be disconnected. This problem is also discussed in the main text (Section II A), using the example presented in Fig. 2. However, the main text offers no numerical details. These details are provided below. 

We consider the CPM quality function with a resolution of _γ_ = 7[1][.][In][the][example][presented][in][Fig.][2][,][the][edges] between nodes 0 and 1 and between nodes 0 and 4 have a weight of 2, as indicated by the thick lines in the figure. All other edges have a weight of 1. The Louvain algorithm starts from a singleton partition, with each node being assigned to its own community. The algorithm then keeps iterating over all nodes, moving each node to its optimal community. Depending on the order in which the nodes are visited, the following could happen. Node 1 is visited first, followed by node 4. Nodes 1 and 4 join the community of node 0, because the weight of the edges between nodes 0 and 1 and between nodes 0 and 4 is sufficiently high. For node 1, the best move clearly is to join the community of node 0. For node 4, the benefit of joining the community of nodes 0 and 1 then is 2 _− γ ·_ 2 =[12] 7[.][This is larger than the] benefit of joining the community of node 5 or 6, which is 1 _− γ ·_ 1 =[6] 7[.][Next,][nodes 2,][3,][5 and 6 are visited.][For these] nodes, it is beneficial to join the community of nodes 0, 1 and 4, because joining this community has a benefit of at 

14 

1: **function** Louvain(Graph _G_ , Partition _P_ ) 

2: **do** 3: _P ←_ MoveNodes( _G, P_ ) 4: done _←|P|_ = _|V_ ( _G_ ) _|_ 5: **if** not done **then** 6: _G ←_ AggregateGraph( _G, P_ ) 7: _P ←_ SingletonPartition( _G_ ) 8: **end if** 9: **while** not done 10: **return** flat _[∗]_ ( _P_ ) 

_▷_ Move nodes between communities _▷_ Terminate when each community consists of only one node 

_▷_ Create aggregate graph based on partition _P ▷_ Assign each node in aggregate graph to its own community 

11: **end function** 

12: **function** MoveNodes(Graph _G_ , Partition _P_ ) 13: **do** 14: _H_ old = _H_ ( _P_ ) 15: **for** _v ∈ V_ ( _G_ ) **do** 16: _C[′] ←_ arg max _C∈P∪∅_ ∆ _HP_ ( _v �→ C_ ) 17: **if** ∆ _HP_ ( _v �→ C[′]_ ) _>_ 0 **then** 18: _v �→ C[′]_ 19: **end if** 20: **end for** 21: **while** _H_ ( _P_ ) _> H_ old 22: **return** _P_ 23: **end function** 

_▷_ Visit nodes (in random order) _▷_ Determine best community for node _v ▷_ Perform only strictly positive node movements _▷_ Move node _v_ to community _C[′]_ 

_▷_ Continue until no more nodes can be moved 

24: **function** AggregateGraph(Graph _G_ , Partition _P_ ) 25: _V ← P_ 26: _E ←{_ ( _C, D_ ) _|_ ( _u, v_ ) _∈ E_ ( _G_ ) _, u ∈ C ∈ P, v ∈ D ∈ P}_ 27: **return** Graph( _V, E_ ) 28: **end function** 

_▷_ Communities become nodes in aggregate graph _▷E_ is a multiset 

29: **function** SingletonPartition(Graph _G_ ) 30: **return** _{{v} | v ∈ V_ ( _G_ ) _}_ 31: **end function** 

_▷_ Assign each node to its own community 

ALGORITHM A.1. **Louvain algorithm.** 

least 1 _− γ ·_ 6 =[1] 7 _[>]_[ 0.][This][then][yields][the][situation][portrayed][in][Fig.][2][(a).][After][some][node][movements][in][the][rest] of the graph, some neighbours of node 0 in the rest of the graph end up together in a new community. Consequently, when node 0 is visited, it can best be moved to this new community, which gives the situation depicted in Fig. 2(b). In particular, suppose there are 5 nodes in the new community, all of which are connected to node 0. In that case, the benefit for node 0 of moving to this community is 5 _− γ ·_ 5 =[30] 7[,][while the benefit of staying in the current community] is only 2 _·_ 2 _− γ ·_ 6 =[22] 7[.][After][node][0][has][moved,][nodes][1][and][4][are][still][locally][optimally][assigned.][For][these][nodes,] the benefit of moving to the new community of node 0 is 2 _− γ ·_ 6 =[8] 7[.][This][is][smaller][than][the][benefit][of][staying] in the current community, which is 2 _− γ ·_ 5 =[9] 7[.][Finally,][nodes][2,][3,][5][and][6][are][all][locally][optimally][assigned,][as] 1 _− γ ·_ 5 =[2] 7 _[>]_[ 0.][Hence,][we][end][up][with][a][community][that][is][disconnected.][In][later][stages][of][the][Louvain][algorithm,] there will be no possibility to repair this. 

The example presented above considers a weighted graph, but this graph can be assumed to be an aggregate graph of an unweighted base graph, thus extending the example also to unweighted graphs. Although the example uses the CPM quality function, similar examples can be given for modularity. However, because of the dependency of modularity on the number of edges _m_ , the calculations for modularity are a bit more complex. Importantly, both for CPM and for modularity, the Louvain algorithm suffers from the problem of disconnected communities. 

## **Appendix C: Reachability of optimal partitions** 

In this appendix, we consider two types of move sequences: non-decreasing move sequences and greedy move sequences. For each type of move sequence, we study whether all optimal partitions are reachable. We first show that this is not the case for greedy move sequences. In particular, we show that for some optimal partitions there does not exist a greedy move sequence that is able to reach the partition. We then show that optimal partitions can always 

15 

1: **function** Leiden(Graph _G_ , Partition _P_ ) 2: **do** 3: _P ←_ MoveNodesFast( _G, P_ ) 4: done _←|P|_ = _|V_ ( _G_ ) _|_ 5: **if** not done **then** 6: _P_ refined _←_ RefinePartition( _G, P_ ) 7: _G ←_ AggregateGraph( _G, P_ refined) 8: _P ←{{v | v ⊆ C, v ∈ V_ ( _G_ ) _} | C ∈ P}_ 9: **end if** 10: **while** not done 11: **return** flat _[∗]_ ( _P_ ) 12: **end function** 

_▷_ Move nodes between communities _▷_ Terminate when each community consists of only one node 

_▷_ Refine partition _P_ 

_▷_ Create aggregate graph based on refined partition _P_ refined _▷_ But maintain partition _P_ 

13: **function** MoveNodesFast(Graph _G_ , Partition _P_ ) 14: _Q ←_ Queue( _V_ ( _G_ )) 15: **do** 16: _v ← Q_ .remove() 17: _C[′] ←_ arg max _C∈P∪∅_ ∆ _HP_ ( _v �→ C_ ) 18: **if** ∆ _HP_ ( _v �→ C[′]_ ) _>_ 0 **then** 19: _v �→ C[′]_ 20: _N ←{u |_ ( _u, v_ ) _∈ E_ ( _G_ ) _, u ∈/ C[′] }_ 21: _Q_ .add( _N − Q_ ) 22: **end if** 23: **while** _Q ̸_ = _∅_ 24: **return** _P_ 25: **end function** 

_▷_ Make sure that all nodes will be visited (in random order) 

_▷_ Determine next node to visit _▷_ Determine best community for node _v ▷_ Perform only strictly positive node movements _▷_ Move node _v_ to community _C[′] ▷_ Identify neighbours of node _v_ that are not in community _C[′] ▷_ Make sure that these neighbours will be visited 

_▷_ Continue until there are no more nodes to visit 

26: **function** RefinePartition(Graph _G_ , Partition _P_ ) 27: _P_ refined _←_ SingletonPartition( _G_ ) 28: **for** _C ∈ P_ **do** 29: _P_ refined _←_ MergeNodesSubset( _G, P_ refined _, C_ ) 30: **end for** 31: **return** _P_ refined 32: **end function** 

_▷_ Assign each node to its own community _▷_ Visit communities _▷_ Refine community _C_ 

33: **function** MergeNodesSubset(Graph _G_ , Partition _P_ , Subset _S_ ) 34: _R_ = _{v | v ∈ S, E_ ( _v, S − v_ ) _≥ γ∥v∥·_ ( _∥S∥−∥v∥_ ) _} ▷_ Consider only nodes that are well connected within subset _S_ 35: **for** _v ∈ R_ **do** _▷_ Visit nodes (in random order) 36: **if** _v_ in singleton community **then** _▷_ Consider only nodes that have not yet been merged 37: _T ←{C | C ∈ P, C ⊆ S, E_ ( _C, S − C_ ) _≥ γ∥C∥·_ ( _∥S∥−∥C∥_ ) _} ▷_ Consider only well-connected communities 38: Pr( _C[′]_ = _C_ ) _∼_ exp[�] _θ_[1][∆] _[H][P]_[(] _[v][�→][C]_[)][�] if ∆ _HP_ ( _v �→ C_ ) _≥_ 0 for _C ∈ T ▷_ Choose random community _C[′]_ �0 otherwise 39: _v �→ C[′] ▷_ Move node _v_ to community _C[′]_ 40: **end if** 41: **end for** 42: **return** _P_ 43: **end function** 

44: **function** AggregateGraph(Graph _G_ , Partition _P_ ) 45: _V ← P_ 46: _E ←{_ ( _C, D_ ) _|_ ( _u, v_ ) _∈ E_ ( _G_ ) _, u ∈ C ∈ P, v ∈ D ∈ P}_ 47: **return** Graph( _V, E_ ) 48: **end function** 

_▷_ Communities become nodes in aggregate graph _▷E_ is a multiset 

49: **function** SingletonPartition(Graph _G_ ) 50: **return** _{{v} | v ∈ V_ ( _G_ ) _}_ 51: **end function** 

_▷_ Assign each node to its own community 

ALGORITHM A.2. **Leiden algorithm.** 

16 

be reached using a non-decreasing move sequence. This result forms the basis for the asymptotic guarantees of the Leiden algorithm, which are discussed in Appendix D 3. 

We first define the different types of move sequences. 

**Definition 4.** Let _G_ = ( _V, E_ ) be a graph, and let _P_ 0 _, . . . , Pτ_ be partitions of _G_ . A sequence of partitions _P_ 0 _, . . . , Pτ_ is called a _move sequence_ if for each _t_ = 0 _, . . . , τ −_ 1 there exists a node _vt ∈ V_ and a community _Ct ∈ Pt ∪∅_ such that _Pt_ +1 = _Pt_ ( _vt �→ Ct_ ). A move sequence is called _non-decreasing_ if _H_ ( _Pt_ +1) _≥ H_ ( _Pt_ ) for all _t_ = 0 _, . . . , τ −_ 1. A move sequence is called _greedy_ if _H_ ( _Pt_ +1) = max _C H_ ( _Pt_ ( _vt �→ C_ )) for all _t_ = 0 _, . . . , τ −_ 1. 

In other words, the next partition in a move sequence is obtained by moving a single node to a different community. Clearly, a greedy move sequence must be non-decreasing, but a non-decreasing move sequence does not need to be greedy. A natural question is whether for any optimal partition _P[∗]_ there exists a move sequence that starts from the singleton partition and that reaches the optimal partition, i.e., a move sequence _P_ 0 _, . . . , Pτ_ with _P_ 0 = _{{v} | v ∈ V }_ and _Pτ_ = _P[∗]_ . Trivially, it is always possible to reach the optimal partition if we allow all moves—even moves that decrease the quality function—as is done for example in simulated annealing [4, 8]. However, it can be shown that there is no need to consider all moves in order to reach the optimal partition. It is sufficient to consider only nondecreasing moves. On the other hand, considering only greedy moves turns out to be too restrictive to guarantee that the optimal partition can be reached. 

## **1. Non-decreasing move sequences** 

We here prove that for any graph there exists a non-decreasing move sequence that reaches the optimal partition _P[∗]_ . The optimal partition can be reached in _n −|P[∗] |_ steps. 

**Theorem 1.** Let _G_ = ( _V, E_ ) be a graph, and let _P[∗]_ be an optimal partition of _G_ . There then exists a non-decreasing move sequence _P_ 0 _, . . . , Pτ_ with _P_ 0 = _{{v} | v ∈ V }_ , _Pτ_ = _P[∗]_ , and _τ_ = _n −|P[∗] |_ . 

_Proof._ Let _C[∗] ∈ P[∗]_ be a community in the optimal partition _P[∗]_ , let _v_ 0 _∈ C[∗]_ be a node in this community, and let _C_ 0 = _{v_ 0 _}_ . Let _P_ 0 = _{{v} | v ∈ V }_ be the singleton partition. For _t_ = 1 _, . . . , |C[∗] | −_ 1, let _vt ∈ C[∗] − Ct−_ 1, let _Ct_ = _{v_ 0 _, . . . , vt} ∈ Pt_ , and let _Pt_ = _Pt−_ 1( _vt �→ Ct−_ 1). We prove by contradiction that there always exists a non-decreasing move sequence _P_ 0 _, . . . , P|C∗|−_ 1. Assume that for some _t_ there does not exist a node _vt_ for which ∆ _H_ ( _vt �→ Ct−_ 1) _≥_ 0. Let _S_ = _C[∗] − Ct−_ 1 and _R_ = _Ct−_ 1. For all _v ∈ S_ , 

**==> picture [112 x 11] intentionally omitted <==**

This implies that 

**==> picture [160 x 22] intentionally omitted <==**

However, by optimality, for all _S ⊆ C[∗]_ and _R_ = _C[∗] − S_ , 

**==> picture [98 x 11] intentionally omitted <==**

We therefore have a contradiction. Hence, there always exists a non-decreasing move sequence _P_ 0 _, . . . , P|C∗|−_ 1. This move sequence reaches the community _Ct_ = _C[∗]_ . The above reasoning can be applied to each community _C[∗] ∈ P[∗]_ . Consequently, each of these communities can be reached using a non-decreasing move sequence. In addition, for each community _C[∗] ∈ P[∗]_ , this can be done in _|C[∗] | −_ 1 steps, so that in total _τ_ =[�] _C[∗] ∈P[∗]_[(] _[|][C][∗][| −]_[1) =] _[ n][ −|][P][∗][|]_[steps][are] needed. ■ 

## **2. Greedy move sequences** 

We here show that there does not always exist a greedy move sequence that reaches the optimal partition of a graph. To show this, we provide a counterexample in which we have a graph for which there is no greedy move sequence that reaches the optimal partition. Our counterexample includes two nodes that should be assigned to different communities. However, because there is a strong connection between the nodes, in a greedy move sequence the nodes are always assigned to the same community. We use the CPM quality function in our counterexample, but a similar counterexample can be given for modularity. The counterexample is illustrated in Fig. C.1. The thick edges 

17 

**==> picture [238 x 188] intentionally omitted <==**

**----- Start of picture text -----**<br>
a)<br>3 7<br>2 0 1 5<br>4 6<br>b)<br>3 7<br>2 0 1 5<br>4 6<br>**----- End of picture text -----**<br>


FIG. C.1. **Unreachable optimal partition.** A greedy move sequence always reaches the partition in (a), whereas the partition in (b) is optimal. This demonstrates that for some graphs there does not exist a greedy move sequence that reaches the optimal partition. 

have a weight of 3, while the thin ones have a weight of[3] 2[.][The][resolution][is][set][to] _[γ]_[= 1.][In][this][situation,][nodes][0] and 1 are always joined together in a community. This has a benefit of 3 _− γ_ = 2, which is larger than the benefit of 3 _·_[3][=][3][by][node][0][joining][the][community][of][nodes][2,][3][and][4][or][node][1][joining][the][community][of] 2 _[−][γ][ ·]_[ 3] 2[obtained] nodes 5, 6 and 7. Hence, regardless of the exact node order, the partition reached by a greedy move sequence always consists of three communities. This gives a total quality of 

**==> picture [178 x 25] intentionally omitted <==**

while the optimal partition has only two communities, consisting of nodes _{_ 0 _,_ 2 _,_ 3 _,_ 4 _}_ and _{_ 1 _,_ 5 _,_ 6 _,_ 7 _}_ and resulting in a total quality of 

**==> picture [140 x 25] intentionally omitted <==**

Hence, a greedy move sequence always reaches the partition in Fig. C.1(a), whereas the partition in Fig. C.1(b) is optimal. 

## **Appendix D: Guarantees of the Leiden algorithm** 

In this appendix, we discuss the guarantees provided by the Leiden algorithm. The guarantees of the Leiden algorithm partly rely on the randomness in the algorithm. We therefore require that _θ >_ 0. Before stating the guarantees of the Leiden algorithm, we first define a number of properties. We start by introducing some relatively weak properties, and we then move on to stronger properties. In the following definitions, _P_ is a flat partition of a graph _G_ = ( _V, E_ ). 

**Definition 5** ( _γ_ -separation) **.** We call a pair of communities _C, D ∈ P γ-separated_ if ∆ _H_ ( _C �→ D_ ) = ∆ _H_ ( _D �→ C_ ) _≤_ 0. A community _C ∈ P_ is _γ_ -separated if _C_ is _γ_ -separated with respect to all _D ∈ P_ . A partition _P_ is _γ_ -separated if all _C ∈ P_ are _γ_ -separated. 

**Definition 6** ( _γ_ -connectivity) **.** We call a set of nodes _S ⊆ C ∈ P γ-connected_ if _|S|_ = 1 or if _S_ can be partitioned into two sets _R_ and _T_ such that _E_ ( _R, T_ ) _≥ γ∥R∥· ∥T ∥_ and _R_ and _T_ are _γ_ -connected. A community _C ∈ P_ is _γ_ -connected if _S_ = _C_ is _γ_ -connected. A partition _P_ is _γ_ -connected if all _C ∈ P_ are _γ_ -connected. 

**Definition 7** (Subpartition _γ_ -density) **.** We call a set of nodes _S ⊆ C ∈ P subpartition γ-dense_ if the following two conditions are satisfied: (i) ∆ _H_ ( _S �→∅_ ) _≤_ 0 and (ii) _|S|_ = 1 or _S_ can be partitioned into two sets _R_ and _T_ such that 

18 

_E_ ( _R, T_ ) _≥ γ∥R∥· ∥T ∥_ and _R_ and _T_ are subpartition _γ_ -dense. A community _C ∈ P_ is subpartition _γ_ -dense if _S_ = _C_ is subpartition _γ_ -dense. A partition _P_ is subpartition _γ_ -dense if all _C ∈ P_ are subpartition _γ_ -dense. 

**Definition 8** (Node optimality) **.** We call a community _C ∈ P node optimal_ if ∆ _H_ ( _v �→ D_ ) _≤_ 0 for all _v ∈ C_ and all _D ∈ P_ (or _D_ = _∅_ ). A partition _P_ is node optimal if all _C ∈ P_ are node optimal. 

**Definition 9** (Uniform _γ_ -density) **.** We call a community _C ∈ P uniformly γ-dense_ if ∆ _H_ ( _S �→∅_ ) _≤_ 0 for all _S ⊆ C_ . A partition _P_ is uniformly _γ_ -dense if all _C ∈ P_ are uniformly _γ_ -dense. 

**Definition 10** (Subset optimality) **.** We call a community _C ∈ P subset optimal_ if ∆ _H_ ( _S �→ D_ ) _≤_ 0 for all _S ⊆ C_ and all _D ∈ P_ (or _D_ = _∅_ ). A partition _P_ is subset optimal if all _C ∈ P_ are subset optimal. 

Subset optimality clearly is the strongest property and subsumes all other properties. Uniform _γ_ -density is subsumed by subset optimality but may be somewhat more intuitive to grasp. It states that any subset of nodes in a community is always connected to the rest of the community with a density of at least _γ_ . In other words, for all _S ⊆ C ∈ P_ we have 

**==> picture [323 x 11] intentionally omitted <==**

Imposing the restriction _D_ = _∅_ in the definition of subset optimality gives the property of uniform _γ_ -density, restricting _S_ to consist of only one node gives the property of node optimality, and imposing the restriction _S_ = _C_ yields the property of _γ_ -separation. Uniform _γ_ -density implies subpartition _γ_ -density, which in turn implies _γ_ -connectivity. Subpartition _γ_ -density also implies that individual nodes cannot be split from their community (but notice that this is a weaker property than node optimality). Ordinary connectivity is implied by _γ_ -connectivity, but not vice versa. Obviously, any optimal partition is subset optimal, but not the other way around: a subset optimal partition is not necessarily an optimal partition (see Fig. C.1(a) for an example). 

In the rest of this appendix, we show that the Leiden algorithm guarantees that the above properties hold for partitions produced by the algorithm. The properties hold either in each iteration, in every stable iteration, or asymptotically. The first two properties of _γ_ -separation and _γ_ -connectivity are guaranteed in each iteration of the Leiden algorithm. We prove this in Appendix D 1. The next two properties of subpartition _γ_ -density and node optimality are guaranteed in every stable iteration of the Leiden algorithm, as we prove in Appendix D 2. Finally, in Appendix D 3 we prove that asymptotically the Leiden algorithm guarantees the last two properties of uniform _γ_ -density and subset optimality. 

## **1. Guarantees in each iteration** 

In order to show that the property of _γ_ -separation is guaranteed in each iteration of the Leiden algorithm, we first need to prove some results for the MoveNodesFast function in the Leiden algorithm. 

We start by introducing some notation. The MoveNodesFast function iteratively evaluates nodes. When a node is evaluated, either it is moved to a different (possibly empty) community or it is kept in its current community, depending on what is most beneficial for the quality function. Let _G_ = ( _V, E_ ) be a graph, let _P_ be a partition of _G_ , and let _P[′]_ = MoveNodesFast( _G, P_ ). We denote by _P_ 0 _, . . . , Pr_ a sequence of partitions generated by the MoveNodesFast function, with _P_ 0 = _P_ denoting the initial partition, _P_ 1 denoting the partition after the first evaluation of a node has taken place, and so on. _Pr_ = _P[′]_ denotes the partition after the final evaluation of a node has taken place. The MoveNodesFast function maintains a queue of nodes that still need to be evaluated. Let _Qs_ be the set of nodes that still need to be evaluated after _s_ node evaluations have taken place, with _Q_ 0 = _V_ . Also, for all _v ∈ V_ , let _Cs[v][∈][P][s]_[be][the][community][in][which][node] _[v]_[finds][itself][after] _[s]_[node][evaluations][have][taken][place.] The following lemma states that at any point in the MoveNodesFast function, if a node is disconnected from the rest of its community, the node will find itself in the queue of nodes that still need to be evaluated. 

**Lemma 2.** Using the notation introduced above, for all _v ∈ V_ and all _s_ , we have _v ∈ Qs_ or _|Cs[v][|]_[ = 1 or] _[ E]_[(] _[v, C] s[v][−][v]_[)] _[ >]_[ 0.] 

_Proof._ We are going to prove the lemma for an arbitrary node _v ∈ V_ . We provide a proof by induction. We observe that _v ∈ Q_ 0, which provides our inductive base. Suppose that _v ∈ Qs−_ 1 or _|Cs[v] −_ 1 _[|]_[ = 1][or] _[E]_[(] _[v, C] s[v] −_ 1 _[−][v]_[)] _[ >]_[ 0.][This][is] our inductive hypothesis. We are going to show that _v ∈ Qs_ or _|Cs[v][|]_[ = 1][or] _[E]_[(] _[v, C] s[v][−][v]_[)] _[ >]_[ 0.][If] _[v][∈][Q][s]_[,][this][result][is] obtained in a trivial way. Suppose therefore that _v ∈/ Qs_ . We then need to show that _|Cs[v][|]_[=][1][or] _[E]_[(] _[v, C] s[v][−][v]_[)] _[>]_[0.] To do so, we distinguish between two cases. 

We first consider the case in which _v ∈ Qs−_ 1. If _v ∈ Qs−_ 1 and _v ∈/ Qs_ , node _v_ has just been evaluated. We then obviously have _|Cs[v][|]_[ = 1][or] _[E]_[(] _[v, C] s[v][−][v]_[)] _[ >]_[ 0.][Otherwise][we][would][have] _[|][C] s[v][|][ >]_[ 1][and] _[E]_[(] _[v, C] s[v][−][v]_[) = 0,][which][would] 

19 

mean that node _v_ is disconnected from the rest of its community. Since node _v_ has just been evaluated, this is not possible. 

We now consider the case in which _v ∈/ Qs−_ 1. Let _u ∈ V_ be the node that has just been evaluated, i.e., _u ∈ Qs−_ 1 and _u ∈/ Qs_ . If node _u_ has not been moved to a different community, then _Ps_ = _Ps−_ 1. Obviously, if _|Cs[v] −_ 1 _[|]_[=][1][or] _E_ ( _v, Cs[v] −_ 1 _[−][v]_[)] _[>]_[0,][we][then][have] _[|][C] s[v][|]_[=][1][or] _[E]_[(] _[v, C] s[v][−][v]_[)] _[>]_[0.][On][the][other][hand,][if][node] _[u]_[has][been][moved][to][a] different community, we have ( _u, v_ ) _∈/ E_ ( _G_ ) or _v ∈ Cs[u]_[.][To][see][this,][note][that][if][(] _[u, v]_[)] _[ ∈][E]_[(] _[G]_[)][and] _[v][∈][/][C] s[u]_[,][we][would] have _v ∈ Qs_ (following line 21 in Algorithm A.2). This contradicts our assumption that _v ∈/ Qs_ , so that we must have ( _u, v_ ) _∈/ E_ ( _G_ ) or _v ∈ Cs[u]_[.][In][other][words,][either][there][is][no][edge][between][nodes] _[u]_[and] _[v]_[or][node] _[u]_[has][been][moved] to the community of node _v_ . In either case, it is not possible that the movement of node _u_ causes node _v_ to become disconnected from the rest of its community. Hence, in either case, if _|Cs[v] −_ 1 _[|]_[ = 1][or] _[E]_[(] _[v, C] s[v] −_ 1 _[−][v]_[)] _[ >]_[ 0,][then] _[|][C] s[v][|]_[ = 1] or _E_ ( _v, Cs[v][−][v]_[)] _[ >]_[ 0.] ■ 

Using Lemma 2, we now prove the following lemma, which states that for partitions provided by the MoveNodesFast function it is guaranteed that singleton communities cannot be merged with each other. 

**Lemma 3.** Let _G_ = ( _V, E_ ) be a graph, let _P_ be a partition of _G_ , and let _P[′]_ = MoveNodesFast( _G, P_ ). Then for all pairs _C, D ∈ P[′]_ such that _|C|_ = _|D|_ = 1, we have ∆ _H_ ( _C �→ D_ ) = ∆ _H_ ( _D �→ C_ ) _≤_ 0. 

_Proof._ We are going to prove the lemma for an arbitrary pair of communities _C, D ∈ P[′]_ such that _|C|_ = _|D|_ = 1. We use the notation introduced above. If _C, D ∈ Ps_ for all _s_ , it is clear that ∆ _H_ ( _C �→ D_ ) = ∆ _H_ ( _D �→ C_ ) _≤_ 0. Otherwise, consider _t_ such that _C, D ∈ Ps_ for all _s ≥ t_ and either _C ∈/ Pt−_ 1 or _D ∈/ Pt−_ 1. Without loss of generality, we assume that _C ∈/ Pt−_ 1 and _D ∈ Pt−_ 1. Consider _v ∈ V_ such that _C_ = _{v}_ . After _t −_ 1 node evaluations have taken place, there are two possibilities. 

One possibility is that node _v_ is evaluated and is moved to an empty community. This means that moving node _v_ to an empty community is more beneficial for the quality function than moving node _v_ to community _D_ . It is then clear that ∆ _H_ ( _C �→ D_ ) = ∆ _H_ ( _D �→ C_ ) _≤_ 0. 

The second possibility is that node _v_ is in a community together with one other node _u ∈ V_ (i.e. _{u, v} ∈ Pt−_ 1) and that this node _u_ is evaluated and is moved to a different community. In this case, _v ∈ Qt_ , as we will now show. If ( _u, v_ ) _∈ E_ ( _G_ ), this follows from line 21 in Algorithm A.2. If ( _u, v_ ) _∈/ E_ ( _G_ ), we have _|Ct[v] −_ 1 _[|]_[=] _[|{][u, v][}|]_[=][2][and] _E_ ( _v, Ct[v] −_ 1 _[−][v]_[) = 0.][It][then][follows][from][Lemma][2][that] _[v][∈][Q][t][−]_[1][.][Since][node] _[v]_[is][not][evaluated][in][node][evaluation] _[t]_ (node _u_ is evaluated in this node evaluation), _v ∈ Qt−_ 1 implies that _v ∈ Qt_ . If _v ∈ Qt_ , at some point _s ≥ t_ , node _v_ is evaluated. Since _C, D ∈ Ps_ for all _s ≥ t_ , keeping node _v_ in its own singleton community _C_ is more beneficial for the quality function than moving node _v_ to community _D_ . This means that ∆ _H_ ( _C �→ D_ ) = ∆ _H_ ( _D �→ C_ ) _≤_ 0. ■ 

Lemma 3 enables us to prove that the property of _γ_ -separation is guaranteed in each iteration of the Leiden algorithm, as stated in the following theorem. 

**Theorem 4.** Let _G_ = ( _V, E_ ) be a graph, let _Pt_ be a flat partition of _G_ , and let _Pt_ +1 = Leiden( _G, Pt_ ). Then _Pt_ +1 is _γ_ -separated. 

_Proof._ Let _Gℓ_ = ( _Vℓ, Eℓ_ ) be the aggregate graph at the highest level in the Leiden algorithm, let _Pℓ_ be the initial partition of _Gℓ_ , and let _Pℓ[′]_[=][MoveNodesFast][(] _[G][ℓ][,][ P][ℓ]_[).][Since][we][are][at][the][highest][level][of][aggregation,][it][follows] from line 4 in Algorithm A.2 that _|Pℓ[′][|]_[=] _[|][V][ℓ][|]_[,][which][means][that] _[|][C][|]_[=][1][for][all] _[C][∈][P] ℓ[′]_[.][In][other][words,] _[P] ℓ[′]_[is][a] singleton partition of _Gℓ_ . Lemma 3 then implies that for all _C, D ∈ Pℓ[′]_[we][have][∆] _[H]_[(] _[C][�→][D]_[)][=][∆] _[H]_[(] _[D][�→][C]_[)] _[≤]_[0.] Since _Pt_ +1 = flat _[∗]_ ( _Pℓ[′]_[),][it][follows][that][for][all] _[C, D][∈][P][t]_[+1][we][have][∆] _[H]_[(] _[C][�→][D]_[) = ∆] _[H]_[(] _[D][�→][C]_[)] _[ ≤]_[0.][Hence,] _[P][t]_[+1][is] _γ_ -separated. ■ 

The property of _γ_ -separation also holds after each iteration of the Louvain algorithm. In fact, for the Louvain algorithm this is much easier to see than for the Leiden algorithm. The Louvain algorithm uses the MoveNodes function instead of the MoveNodesFast function. Unlike the MoveNodesFast function, the MoveNodes function yields partitions that are guaranteed to be node optimal. This guarantee leads in a straightforward way to the property of _γ_ -separation for partitions obtained in each iteration of the Louvain algorithm. 

We now consider the property of _γ_ -connectivity. By constructing a tree corresponding to the decomposition of _γ_ -connectivity, we are going to prove that this property is guaranteed in each iteration of the Leiden algorithm. 

**Theorem 5.** Let _G_ = ( _V, E_ ) be a graph, let _Pt_ be a flat partition of _G_ , and let _Pt_ +1 = Leiden( _G, Pt_ ). Then _Pt_ +1 is _γ_ -connected. 

_Proof._ Let _Gℓ_ = ( _Vℓ, Eℓ_ ) be the aggregate graph at level _ℓ_ in the Leiden algorithm, with _G_ 0 = _G_ being the base graph. We say that a node _v ∈ Vℓ_ is _γ_ -connected if flat( _v_ ) is _γ_ -connected. We are going to proceed inductively. Each node in the base graph _G_ 0 is trivially _γ_ -connected. This provides our inductive base. Suppose that each node _v ∈ Vℓ−_ 1 is 

20 

_γ_ -connected, which is our inductive hypothesis. Each node _v ∈ Vℓ_ is obtained by merging one or more nodes at the preceding level, i.e. _v_ = _{u | u ∈ S}_ for some set _S ⊆ Vℓ−_ 1. If _v_ consists of only one node at the preceding level, _v_ is immediately _γ_ -connected by our inductive hypothesis. The set of nodes _S_ is constructed in the MergeNodesSubset function. There exists some order _u_ 1 _, . . . , uk_ in which nodes are added to _S_ . Let _Si_ = _{u_ 1 _, . . . , ui}_ be the set obtained after adding node _ui_ . It follows from line 38 in Algorithm A.2 that _E_ ( _ui_ +1 _, Si_ ) _≥ γ∥ui_ +1 _∥· ∥Si∥_ for _i_ = 1 _, . . . , k −_ 1. Taking into account that each _ui_ is _γ_ -connected by our inductive hypothesis, this implies that each set _Si_ is _γ_ - connected. Since _S_ = _Sk_ is _γ_ -connected, node _v_ is _γ_ -connected. Hence, each node _v ∈ Vℓ_ is _γ_ -connected. This also holds for the nodes in the aggregate graph at the highest level in the Leiden algorithm, which implies that all communities in _Pt_ +1 are _γ_ -connected. In other words, _Pt_ +1 is _γ_ -connected. ■ 

Note that the theorem does not require _Pt_ to be connected. Even if a disconnected partition is provided as input to the Leiden algorithm, performing a single iteration of the algorithm will give a partition that is _γ_ -connected. 

## **2. Guarantees in stable iterations** 

As discussed earlier, the Leiden algorithm can be iterated until _Pt_ +1 = Leiden( _G, Pt_ ). Likewise, the Louvain algorithm can be iterated until _Pt_ +1 = Louvain( _G, Pt_ ). We say that an iteration is _stable_ if _Pt_ +1 = _Pt_ , in which case we call _Pt_ (or _Pt_ +1) a _stable partition_ . 

There is a subtle point when considering stable iterations. In order for the below guarantees to hold, we need to ensure that _H_ ( _Pt_ +1) = _H_ ( _Pt_ ) implies _Pt_ +1 = _Pt_ . In both the Leiden algorithm and the Louvain algorithm, we therefore consider only strictly positive improvements (see line 17 in Algorithm A.1 and line 18 in Algorithm A.2). In other words, if a node movement leads to a partition that has the same quality as the current partition, the current partition is preferred and the node movement will not take place. This then also implies that _H_ ( _Pt_ +1) _> H_ ( _Pt_ ) if _Pt_ +1 = _Pt_ . 

The Leiden algorithm guarantees that a stable partition is subpartition _γ_ -dense, as stated in the following theorem. Note that the proof of the theorem has a structure that is similar to the structure of the proof of Theorem 5 presented above. 

**Theorem 6.** Let _G_ = ( _V, E_ ) be a graph, let _Pt_ be a flat partition of _G_ , and let _Pt_ +1 = Leiden( _G, Pt_ ). If _Pt_ +1 = _Pt_ , then _Pt_ +1 = _Pt_ is subpartition _γ_ -dense. 

_Proof._ Suppose we have a stable iteration. Hence, _Pt_ +1 = _Pt_ . Let _Gℓ_ = ( _Vℓ, Eℓ_ ) be the aggregate graph at level _ℓ_ in the Leiden algorithm, with _G_ 0 = _G_ being the base graph. We say that a node _v ∈ Vℓ_ is subpartition _γ_ -dense if the set of nodes flat( _v_ ) is subpartition _γ_ -dense. We first observe that for all levels _ℓ_ and all nodes _v ∈ Vℓ_ we have ∆ _H_ ( _v �→∅_ ) _≤_ 0. To see this, note that if ∆ _H_ ( _v �→∅_ ) _>_ 0 for some level _ℓ_ and some node _v ∈ Vℓ_ , the MoveNodesFast function would have removed node _v_ from its community, which means that the iteration would not have been stable. We are now going to proceed inductively. Since ∆ _H_ ( _v �→∅_ ) _≤_ 0 for all nodes _v ∈ V_ 0, each node in the base graph _G_ 0 is subpartition _γ_ -dense. This provides our inductive base. Suppose that each node _v ∈ Vℓ−_ 1 is subpartition _γ_ -dense, which is our inductive hypothesis. Each node _v ∈ Vℓ_ is obtained by merging one or more nodes at the preceding level, i.e. _v_ = _{u | u ∈ S}_ for some set _S ⊆ Vℓ−_ 1. If _v_ consists of only one node at the preceding level, _v_ is immediately subpartition _γ_ -dense by our inductive hypothesis. The set of nodes _S_ is constructed in the MergeNodesSubset function. There exists some order _u_ 1 _, . . . , uk_ in which nodes are added to _S_ . Let _Si_ = _{u_ 1 _, . . . , ui}_ be the set obtained after adding node _ui_ . It follows from line 38 in Algorithm A.2 that _E_ ( _ui_ +1 _, Si_ ) _≥ γ∥ui_ +1 _∥·∥Si∥_ for _i_ = 1 _, . . . , k −_ 1. Furthermore, line 37 in Algorithm A.2 ensures that ∆ _H_ ( _Si �→∅_ ) _≤_ 0 for _i_ = 1 _, . . . , k −_ 1. We also have ∆ _H_ ( _Sk �→∅_ ) _≤_ 0, since _Sk_ = _S_ = _v_ and since ∆ _H_ ( _v �→∅_ ) _≤_ 0, as observed above. Taking into account that each _ui_ is subpartition _γ_ -dense by our inductive hypothesis, this implies that each set _Si_ is subpartition _γ_ -dense. Since _S_ = _Sk_ is subpartition _γ_ -dense, node _v_ is subpartition _γ_ -dense. Hence, each node _v ∈ Vℓ_ is subpartition _γ_ -dense. This also holds for the nodes in the aggregate graph at the highest level in the Leiden algorithm, which implies that all communities in _Pt_ +1 = _Pt_ are subpartition _γ_ -dense. In other words, _Pt_ +1 = _Pt_ is subpartition _γ_ -dense. ■ 

Subpartition _γ_ -density does not imply node optimality. It guarantees only that ∆ _H_ ( _v �→∅_ ) _≤_ 0 for all _v ∈ V_ , not that ∆ _H_ ( _v �→ D_ ) _≤_ 0 for all _v ∈ V_ and all _D ∈ P_ . However, it is easy to see that all nodes are locally optimally assigned in a stable iteration of the Leiden algorithm. This is stated in the following theorem. 

**Theorem 7.** Let _G_ = ( _V, E_ ) be a graph, let _Pt_ be a flat partition of _G_ , and let _Pt_ +1 = Leiden( _G, Pt_ ). If _Pt_ +1 = _Pt_ , then _Pt_ +1 = _Pt_ is node optimal. 

21 

_Proof._ Suppose we have a stable iteration. Hence, _Pt_ +1 = _Pt_ . We are going to give a proof by contradiction. Assume that _Pt_ +1 = _Pt_ is not node optimal. There then exists a node _v ∈ C ∈ Pt_ and a community _D ∈ Pt_ (or _D_ = _∅_ ) such that ∆ _H_ ( _v �→ D_ ) _>_ 0. The MoveNodesFast function then moves node _v_ to community _D_ . This means that _Pt_ +1 = _Pt_ and that the iteration is not stable. We now have a contradiction, which implies that the assumption of _Pt_ +1 = _Pt_ not being node optimal must be false. Hence, _Pt_ +1 = _Pt_ is node optimal. ■ 

In the same way, it is straightforward to see that the Louvain algorithm also guarantees node optimality in a stable iteration. 

When the Louvain algorithm reaches a stable iteration, the partition is _γ_ -separated and node optimal. Since the Louvain algorithm considers only moving nodes and merging communities, additional iterations of the algorithm will not lead to further improvements of the partition. Hence, in the case of the Louvain algorithm, if _Pt_ +1 = _Pt_ , then _Pτ_ = _Pt_ for all _τ ≥ t_ . In other words, when the Louvain algorithm reaches a stable iteration, all future iterations will be stable as well. This contrasts with the Leiden algorithm, which may continue to improve a partition after a stable iteration. We consider this in more detail below. 

## **3. Asymptotic guarantees** 

When an iteration of the Leiden algorithm is stable, this does not imply that the next iteration will also be stable. Because of randomness in the refinement phase of the Leiden algorithm, a partition that is stable in one iteration may be improved in the next iteration. However, at some point, a partition will be obtained for which the Leiden algorithm is unable to make any further improvements. We call this an asymptotically stable partition. Below, we prove that an asymptotically stable partition is uniformly _γ_ -dense and subset optimal. 

We first need to show what it means to define asymptotic properties for the Leiden algorithm. The Leiden algorithm considers moving a node to a different community only if this results in a strict increase in the quality function. As stated in the following lemma, this ensures that at some point the Leiden algorithm will find a partition for which it can make no further improvements. 

**Lemma 8.** Let _G_ = ( _V, E_ ) be a graph, and let _Pt_ +1 = Leiden( _G, Pt_ ). There exists a _τ_ such that _Pt_ = _Pτ_ for all _t ≥ τ_ . 

_Proof._ Only strict improvements can be made in the Leiden algorithm. Consequently, if _Pt_ +1 = _Pt_ , then _Pt_ +1 = _Pt′_ for all _t[′] ≤ t_ . Assume that there does not exist a _τ_ such that _Pt_ = _Pτ_ for all _t ≥ τ_ . Then for any _τ_ there exists a _t > τ_ such that _Pt_ = _Pt′_ for all _t[′] < t_ . This implies that the number of unique elements in the sequence _P_ 0 _, P_ 1 _, . . ._ is infinite. However, this is not possible, because the number of partitions of _G_ is finite. Hence, the assumption that there does not exist a _τ_ such that _Pt_ = _Pτ_ for all _t ≥ τ_ is false. ■ 

According to the above lemma, the Leiden algorithm progresses towards a partition for which no further improvements can be made. We can therefore define the notion of an asymptotically stable partition. 

**Definition 11.** Let _G_ = ( _V, E_ ) be a graph, and let _Pt_ +1 = Leiden( _G, Pt_ ). We call _Pτ asymptotically stable_ if _Pt_ = _Pτ_ for all _t ≥ τ_ . 

We also need to define the notion of a minimal non-optimal subset. 

**Definition 12.** Let _G_ = ( _V, E_ ) be a graph, and let _P_ be a partition of _G_ . A set _S ⊆ C ∈ P_ is called a _non-optimal subset_ if ∆ _H_ ( _S �→ D_ ) _>_ 0 for some _D ∈ P_ or for _D_ = _∅_ . A set _S ⊆ C ∈ P_ is called a _minimal non-optimal subset_ if _S_ is a non-optimal subset and if there does not exist a non-optimal subset _S[′] ⊂ S_ . 

The following lemma states an important property of minimal non-optimal subsets. 

**Lemma 9.** Let _G_ = ( _V, E_ ) be a graph, let _P_ be a partition of _G_ , and let _S ⊆ C ∈ P_ be a minimal non-optimal subset. Then _{S}_ is an optimal partition of the subgraph induced by _S_ . 

_Proof._ Assume that _{S}_ is not an optimal partition of the subgraph induced by _S_ . There then exists a set _S_ 1 _∈ S_ such that 

**==> picture [320 x 11] intentionally omitted <==**

**==> picture [337 x 11] intentionally omitted <==**

**==> picture [377 x 11] intentionally omitted <==**

22 

Because _S_ is a minimal non-optimal subset, _S_ 1 and _S_ 2 cannot be non-optimal subsets. Therefore, ∆ _H_ ( _S_ 1 _→ D_ ) _≤_ 0 and ∆ _H_ ( _S_ 2 _→ D_ ) _≤_ 0, or equivalently, 

**==> picture [389 x 11] intentionally omitted <==**

and 

**==> picture [389 x 11] intentionally omitted <==**

It then follows from Eqs. (D4) and (D5) that 

**==> picture [438 x 29] intentionally omitted <==**

This can be written as 

**==> picture [382 x 43] intentionally omitted <==**

Using Eq. (D2), we then obtain 

**==> picture [244 x 11] intentionally omitted <==**

However, this contradicts Eq. (D3). The assumption that _{S}_ is not an optimal partition of the subgraph induced by _S_ is therefore false. ■ 

Building on the results for non-decreasing move sequences reported in Appendix C 1, the following lemma states that any minimal non-optimal subset can be found by the MergeNodeSubset function. 

**Lemma 10.** Let _G_ = ( _V, E_ ) be a graph, let _P_ be a partition of _G_ , and let _S ⊆ C ∈ P_ be a minimal non-optimal subset. Let _P_ refined = MergeNodesSubset( _G, {{v} | v ∈ V }, C_ ). There then exists a move sequence in the MergeNodesSubset function such that _S ∈ P_ . 

_Proof._ We are going to prove that there exists a move sequence _P_ 0 _, . . . , P|C|_ in the MergeNodesSubset function such that _S ∈ P|C|_ . The move sequence consists of two parts, _P_ 0 _, . . . , P|S|_ and _P|S|, . . . , P|C|_ . In the first part, each node in _S_ is considered for moving. In the second part, each node in _C − S_ is considered for moving. Note that in the MergeNodesSubset function a node can always stay in its own community when it is considered for moving. We first consider the first part of the move sequence _P_ 0 _, . . . , P|C|_ . Let _P_ 0 _, . . . , P|S|_ be a non-decreasing move sequence such that _P_ 0 = _{{v} | v ∈ V }_ and _S ∈ P|S|_ . To see that such a non-decreasing move sequence exists, note that according to Lemma 9 _{S}_ is an optimal partition of the subgraph induced by _S_ and that according to Theorem 1 an optimal partition can be reached using a non-decreasing move sequence. This non-decreasing move sequence consists of _|S| −_ 1 moves. There is one node in _S_ that can stay in its own community. Note further that each move in the move sequence _P_ 0 _, . . . , P|S|_ satisfies the conditions specified in lines 34 and 37 in Algorithm A.2. This follows from Definition 12. In the second part of the move sequence _P_ 0 _, . . . , P|C|_ , we simply have _P|S|_ = _. . ._ = _P|C|_ . Hence, each node in _C − S_ stays in its own community. Since _S ∈ P|S|_ , we then also have _S ∈ P|C|_ . ■ 

As long as there are subsets of communities that are not optimally assigned, the MergeNodesSubset function can find these subsets. In the MoveNodesFast function, these subsets are then moved to a different community. In this way, the Leiden algorithm continues to identify better partitions. However, at some point, all subsets of communities are optimally assigned, and the Leiden algorithm will not be able to further improve the partition. The algorithm has then reached an asymptotically stable partition, and this partition is also subset optimal. This result is formalized in the following theorem. 

**Theorem 11.** Let _G_ = ( _V, E_ ) be a graph, and let _P_ be a flat partition of _G_ . Then _P_ is asymptotically stable if and only if _P_ is subset optimal. 

_Proof._ If _P_ is subset optimal, it follows directly from the definition of the Leiden algorithm that _P_ is asymptotically stable. Conversely, if _P_ is asymptotically stable, it follows from Lemma 10 that _P_ is subset optimal. To see this, assume that _P_ is not subset optimal. There then exists a community _C ∈ P_ and a set _S ⊂ C_ such that _S_ is a minimal non-optimal subset. Let _P_ refined = MergeNodesSubset( _G, {{v} | v ∈ V }, C_ ). Lemma 10 states that there exists a move sequence in the MergeNodesSubset function such that _S ∈ P_ refined. If _S ∈ P_ refined, then _S_ will be moved from _C_ to a different (possibly empty) community in line 3 in Algorithm A.2. However, this contradicts the asymptotic stability of _P_ . Asymptotic stability therefore implies subset optimality. ■ 

23 

Since subset optimality implies uniform _γ_ -density, we obtain the following corollary. 

**Corollary 12.** Let _G_ = ( _V, E_ ) be a graph, and let _P_ be a flat partition of _G_ . If _P_ is asymptotically stable, then _P_ is uniformly _γ_ -dense. 

## **Appendix E: Bounds on optimality** 

In this appendix, we prove that the quality of a uniformly _γ_ -dense partition as defined in Definition 9 in Appendix D provides an upper bound on the quality of an optimal partition. 

We first define the intersection of two partitions. 

**Definition 13.** Let _G_ = ( _V, E_ ) be a graph, and let _P_ 1 and _P_ 2 be flat partitions of _G_ . We denote the _intersection_ of _P_ 1 and _P_ 2 by _P_ = _P_ 1 _⊓ P_ 2, which is defined as 

**==> picture [350 x 11] intentionally omitted <==**

The intersection of two partitions consists of the basic subsets that form both partitions. For _S, R ∈ P_ = _P_ 1 _⊓ P_ 2, we write _S[P] ∼_[1] _R_ if there exists a community _C ∈ P_ 1 such that _S, R ⊆ C_ . Hence, if _S[P] ∼_[1] _R_ , then _S_ and _R_ are subsets of the same community in _P_ 1. Furthermore, for _S_ = _R_ , if _S[P] ∼_[1] _R_ , then we cannot have _S[P] ∼_[2] _R_ , since otherwise _S_ and _R_ would have formed a single subset. In other words, _S[P] ∼_[1] _R ⇒ S[P]_ ≁[2] _R_ and similarly _S[P] ∼_[2] _R ⇒ S[P]_ ≁[1] _R_ . 

The following lemma shows how the difference in quality between two partitions can easily be expressed using the intersection. 

**Lemma 13.** Let _G_ = ( _V, E_ ) be a graph, let _P_ 1 and _P_ 2 be flat partitions of _G_ , and let _P_ = _P_ 1 _⊓ P_ 2 be the intersection of _P_ 1 and _P_ 2. Then 

**==> picture [434 x 39] intentionally omitted <==**

_Proof._ For any community _C ∈ Pk_ ( _k_ = 1 _,_ 2), 

**==> picture [184 x 43] intentionally omitted <==**

and 

**==> picture [190 x 44] intentionally omitted <==**

We hence obtain 

**==> picture [338 x 138] intentionally omitted <==**

The difference _H_ ( _P_ 2) _− H_ ( _P_ 1) then gives the desired result. 

■ 

24 

The above lemma enables us to prove the following theorem, stating that the quality of a uniformly _γ_ -dense partition is not too far from optimal. We stress that this theorem applies only to unweighted graphs. 

**Theorem 14.** Let _G_ = ( _V, E_ ) be an unweighted graph, let _P_ be a uniformly _γ_ -dense partition of _G_ , and let _P[∗]_ be an optimal partition of _G_ . Then 

**==> picture [349 x 35] intentionally omitted <==**

_Proof._ Let _P[′]_ = _P ⊓ P[∗]_ . Consider any _S, R ∈ P[′]_ such that _S[P] ∼[∗] R_ . Because the graph _G_ is unweighted, we have _∥S∥· ∥R∥≥ E_ ( _S, R_ ). It follows that 

**==> picture [174 x 11] intentionally omitted <==**

Furthermore, for any community _C ∈ P_ , the number of edges connecting this community with other communities is _E_ ( _C, V − C_ ). We therefore have 

**==> picture [147 x 35] intentionally omitted <==**

To see this, note that _R[P] ∼[∗] S_ implies _R_ ≁ _[P] S_ , so that _R ̸⊆ C_ . For any _C ∈ P_ , we then obtain 

**==> picture [360 x 35] intentionally omitted <==**

By summing over all _C ∈ P_ , this gives 

**==> picture [233 x 35] intentionally omitted <==**

Furthermore, because _P_ is uniformly _γ_ -dense, we have 

**==> picture [140 x 34] intentionally omitted <==**

Using these results, Eq. (E3) follows from Lemma 13. 

**==> picture [9 x 8] intentionally omitted <==**

For weighted graphs, an upper bound analogous to Eq. (E3) is 

**==> picture [353 x 28] intentionally omitted <==**

where _w_ ¯ = max _i,j wi,j_ is the maximum edge weight. 

For modularity instead of CPM, the upper bound for unweighted graphs in Eq. (E3) needs to be adjusted by rescaling the resolution parameter by 2 _m_ . This gives 

**==> picture [357 x 35] intentionally omitted <==**

The approximation factor of modularity cannot be multiplicative [31], and indeed our bound is additive. Depending on the partition _P_ , our bound may be better than the bound provided by an SDP algorithm [31]. 

25 

Note that the bound in Eq. (E3) reduces the trivial bound of (1 _−γ_ ) _m_ by _γ_ times the number of missing links within communities, i.e., _γ_[�] _C_ �� _∥C_ 2 _∥_ � _− E_ ( _C, C_ )�. To see this, note that _m_ =[�] _C[E]_[(] _[C, C]_[) +][1] 2 � _C_ = _D[E]_[(] _[C, D]_[).][Starting] from Eq. (E3), we then obtain 

**==> picture [310 x 99] intentionally omitted <==**

Finally, Theorem 14 provides a bound on the quality of the optimal partition for a given uniformly _γ_ -dense partition, but it does not provide an a priori bound on the minimal quality of a uniformly _γ_ -dense partition. Finding such an a priori bound remains an open problem. 

