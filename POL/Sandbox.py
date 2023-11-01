# %%
# Loop over all springs
            for spring in cube.springs:
                # If spring connected to that mass
                if spring.m1 == mass or spring.m2 == mass:
                    # Calculate spring force
                    L = np.linalg.norm(spring.m1.p - spring.m2.p)
                    F_spring = spring.k * (L - spring.L0)
                    # Update F_spring in the vector direction from m2 to m1
                    F_spring *= (spring.m1.p - spring.m2.p) / L
                    # Update F with appropriate sign
                    if spring.m1 == mass:
                        F += F_spring
                    else:
                        F -= F_spring