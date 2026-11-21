%% Non-Newtonian (power-law) blood flow through a stenosed artery
%  Starter model: steady, axisymmetric, fully developed flow in a slowly
%  varying tube (lubrication approximation), solved numerically along the artery.
%
%  Blood is shear-thinning, modelled as a power-law fluid:
%       tau = K * (du/dr)^n        (n < 1 shear-thinning, n = 1 Newtonian)
%
%  Stenosis shape (mild, symmetric):
%       R(z) = R0 * ( 1 - (delta/2) * (1 + cos(pi*z/z0)) )   for |z| <= z0
%       R(z) = R0                                           otherwise
%  where delta is the fractional reduction of the radius at the throat.
%
%  For a given volumetric flow rate Q the local pressure gradient G = -dp/dz
%  and wall shear stress follow from the power-law tube solution:
%       tau_w(z) = K * ( Q*(3n+1)/(pi*n) )^n * R(z)^(-3n)
%       G(z)     = 2*tau_w(z) / R(z)
%       u(r,z)   = n/(n+1) * (G/(2K))^(1/n) * ( R^((n+1)/n) - r^((n+1)/n) )
%
%  Outputs (saved in ./outputs): figures and sensitivity_results.csv
%  NOTE: replace / extend the model with your own governing equations as needed.

clear; clc; close all;
if ~exist('outputs', 'dir'), mkdir('outputs'); end

%% 1. Parameters (SI units)
R0    = 3e-3;        % healthy radius (m)
z0    = 10e-3;       % half-length of the stenosis (m)
Lz    = 60e-3;       % length of artery segment modelled (m)
Q     = 2e-6;        % volumetric flow rate (m^3/s)
K     = 0.017;       % consistency index (Pa s^n)
n     = 0.708;       % power-law index
delta = 0.5;         % stenosis severity (fraction of radius lost)
mu    = 0.0035;      % Newtonian reference viscosity (Pa s)

z = linspace(-Lz/2, Lz/2, 1201);

%% 2. Baseline solution
R   = radius(z, R0, z0, delta);
tw  = wallShear(R, Q, K, n);
G   = 2 * tw ./ R;
dp  = trapz(z, G);                       % total pressure drop (Pa)

% Newtonian comparison at the same flow rate
tw_N = wallShear(R, Q, mu, 1);
dp_N = trapz(z, 2 * tw_N ./ R);

fprintf('Baseline (delta = %.2f): max wall shear stress = %.2f Pa, pressure drop = %.1f Pa\n', ...
        delta, max(tw), dp);
fprintf('Newtonian comparison  : max wall shear stress = %.2f Pa, pressure drop = %.1f Pa\n', ...
        max(tw_N), dp_N);

%% 3. Figures: geometry, wall shear stress, pressure gradient
figure('Position', [100 100 1000 700]);
subplot(3,1,1); plot(z*1e3, R*1e3, 'k', z*1e3, -R*1e3, 'k', 'LineWidth', 1.5);
ylabel('Radius (mm)'); title('Stenosed artery geometry'); grid on;
subplot(3,1,2); plot(z*1e3, tw, 'LineWidth', 1.5); hold on;
plot(z*1e3, tw_N, '--', 'LineWidth', 1.5); hold off;
ylabel('Wall shear stress (Pa)'); legend('Power-law', 'Newtonian'); grid on;
subplot(3,1,3); plot(z*1e3, G/1e3, 'LineWidth', 1.5);
ylabel('-dp/dz (kPa/m)'); xlabel('z (mm)'); grid on;
saveas(gcf, 'outputs/geometry_wss_pressure_gradient.png');

%% 4. Velocity profiles at the throat vs. a healthy section
figure; hold on;
for loc = [0, 2*z0]
    Rl  = radius(loc, R0, z0, delta);
    Gl  = 2 * wallShear(Rl, Q, K, n) / Rl;
    r   = linspace(0, Rl, 200);
    u   = n/(n+1) * (Gl/(2*K))^(1/n) * (Rl^((n+1)/n) - r.^((n+1)/n));
    plot([-fliplr(r) r]*1e3, [fliplr(u) u], 'LineWidth', 1.5);
end
hold off; grid on; xlabel('Radial position (mm)'); ylabel('Axial velocity (m/s)');
legend('Throat (z = 0)', 'Healthy section'); title('Velocity profiles');
saveas(gcf, 'outputs/velocity_profiles.png');

%% 5. Numerical check: integrating u over the cross-section should recover Q
Rt = radius(0, R0, z0, delta);
Gt = 2 * wallShear(Rt, Q, K, n) / Rt;
r  = linspace(0, Rt, 4001);
u  = n/(n+1) * (Gt/(2*K))^(1/n) * (Rt^((n+1)/n) - r.^((n+1)/n));
Q_num = trapz(r, 2*pi*r.*u);
fprintf('Flow-rate check at throat: Q_num = %.4e, Q = %.4e (error %.3f%%)\n', ...
        Q_num, Q, 100*abs(Q_num-Q)/Q);

%% 6. Sensitivity analysis: stenosis severity x viscosity (consistency index)
deltas = 0:0.1:0.7;
Kscale = [0.5 1 1.5];
results = [];
for s = Kscale
    for d = deltas
        Rs = radius(z, R0, z0, d);
        tws = wallShear(Rs, Q, s*K, n);
        dps = trapz(z, 2*tws./Rs);
        results = [results; s, d, max(tws), dps]; %#ok<AGROW>
    end
end
T = array2table(results, 'VariableNames', {'K_scale', 'stenosis_severity', 'max_wss_Pa', 'pressure_drop_Pa'});
writetable(T, 'outputs/sensitivity_results.csv');

figure;
for s = Kscale
    m = results(:,1) == s;
    subplot(1,2,1); hold on; plot(results(m,2), results(m,3), '-o', 'LineWidth', 1.5);
    subplot(1,2,2); hold on; plot(results(m,2), results(m,4), '-o', 'LineWidth', 1.5);
end
subplot(1,2,1); xlabel('Stenosis severity \delta'); ylabel('Max wall shear stress (Pa)'); grid on;
legend('0.5 K', '1.0 K', '1.5 K', 'Location', 'northwest');
subplot(1,2,2); xlabel('Stenosis severity \delta'); ylabel('Pressure drop (Pa)'); grid on;
saveas(gcf, 'outputs/sensitivity_analysis.png');
disp('Done. Results saved in ./outputs');

%% ---------- Local functions ----------
function R = radius(z, R0, z0, delta)
    R = R0 * ones(size(z));
    m = abs(z) <= z0;
    R(m) = R0 * (1 - (delta/2) * (1 + cos(pi * z(m) / z0)));
end

function tw = wallShear(R, Q, K, n)
    tw = K * (Q * (3*n + 1) / (pi * n))^n .* R.^(-3*n);
end
