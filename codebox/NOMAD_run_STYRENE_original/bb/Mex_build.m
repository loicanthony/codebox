%% Build for Matlab

switch(computer)
case 'PCWIN'
libdir = ' -Lwin32\';
case 'PCWIN64' 
libdir = ' -Lwin64\';      
case 'GLNX86'
libdir = 'glnx86/';
case 'GLNXA64'
libdir = 'glnxa64/';
case 'MACI64'
libdir = 'maci64/';
end

fprintf('\n------------------------------------------------\n');
fprintf('STYRENE MEX FILE BUILD \n\n');

% Current directory
cdir = cd;

%Get NOMAD Libraries
post = [' -I. -DMEX_RUN -output bb_truth.' mexext ];

%Compile & Move
pre =[ 'mex -v -largeArrayDims styrenmex.cpp bissection.cpp burner.cpp cashflow.cpp chemical.cpp column.cpp combrx.cpp flash.cpp heatx.cpp mix.cpp ' ...
    ' pfr.cpp profitability.cpp pump.cpp reaction.cpp reactor.cpp RungeKutta.cpp secant.cpp servor.cpp split.cpp stream.cpp thermolib.cpp ' ];

try
    eval([pre post])
    fprintf('Compilation done!\n');
catch ME
    error('Error Compiling NOMAD!\n%s',ME.message);
end
