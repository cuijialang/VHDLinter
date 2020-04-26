entity counter is
    port ( clk, rst, dir, ena : in std_ulogic;
            q0, q1 : out std_ulogic);
end counter;

architecture counter_arc of counter is

    component or2
    port (a,b : in std_ulogic;
            y : out std_ulogic);
    end component;

    component and2
    port (a,b : in std_ulogic;
            y : out std_ulogic);
    end component;

    component inv
    port (y : out std_ulogic;
          a : in std_ulogic);
    end component;

    component ff -- TODO
    port (t, clk, rst : in std_ulogic;
          q, qn : out std_ulogic);
    end component;

    signal n0, n1, n2, n3, n4, n5, n6, n7, n8, n9, n10 : std_ulogic;
    begin
        g0 : inv
        port map (dir, n0);
        g1 : and2           
        port map (dir, ena, n1); 
        g2 : and2
        port map (ena, n0, n2);
        g3 : or2
        port map (n1, n2, n3);
        g4 : ff
        port map (n3, clk, rst, n4, n5);
        g5 : and2
        port map (n1, n4, n6);
        g6 : and2
        port map (n2, n5, n7);
        g7 : or2
        port map (n6, n7, n8);
        g8 : ff
        port map (n8, clk, rst, n9, n10);
        q0 <= n4; q1 <= n9;

end counter_arc;
