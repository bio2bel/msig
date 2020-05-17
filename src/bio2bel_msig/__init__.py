# -*- coding: utf-8 -*-

"""Bio2BEL MSig is a package for enriching BEL networks with MsigDB.

Furthermore, it is integrated in the `ComPath environment <https://github.com/ComPath>`_ for pathway database comparison.

Citation
--------
- Subramanian, A., Tamayo, P., Mootha, V. K., Mukherjee, S., Ebert, B. L., Gillette, M. A., ... & Mesirov, J. P.
  (2005). Gene set enrichment analysis: a knowledge-based approach for interpreting genome-wide expression profiles.
  Proceedings of the National Academy of Sciences, 102(43), 15545-15550.
- Liberzon, A., Subramanian, A., Pinchback, R., Thorvaldsdóttir, H., Tamayo, P., & Mesirov, J. P. (2011). Molecular
  signatures database (MSigDB) 3.0. Bioinformatics, 27(12), 1739-1740.
"""

from .manager import Manager
